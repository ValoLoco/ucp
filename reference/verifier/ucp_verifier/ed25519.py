"""Ed25519 (RFC 8032) verify and sign.

Uses the well-known `cryptography` package when installed. Falls back to the
RFC 8032 section 6 reference algorithm so the verifier and test vectors run
with the Python standard library only. The fallback is slow and not
constant-time; it is fine for conformance testing, not for production keys.
"""

from __future__ import annotations

import hashlib

try:  # pragma: no cover - exercised depending on environment
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
    from cryptography.hazmat.primitives import serialization

    BACKEND = "cryptography"
except ImportError:  # pragma: no cover
    BACKEND = "rfc8032-reference"

# ---- RFC 8032 section 6 reference implementation (fallback) ----
_p = 2**255 - 19
_q = 2**252 + 27742317777372353535851937790883648493
_d = -121665 * pow(121666, _p - 2, _p) % _p
_modp_sqrt_m1 = pow(2, (_p - 1) // 4, _p)


def _sha512(s: bytes) -> bytes:
    return hashlib.sha512(s).digest()


def _point_add(P, Q):
    A, B = (P[1] - P[0]) * (Q[1] - Q[0]) % _p, (P[1] + P[0]) * (Q[1] + Q[0]) % _p
    C, D = 2 * P[3] * Q[3] * _d % _p, 2 * P[2] * Q[2] % _p
    E, F, G, H = B - A, D - C, D + C, B + A
    return (E * F, G * H, F * G, E * H)


def _point_mul(s, P):
    Q = (0, 1, 1, 0)
    while s > 0:
        if s & 1:
            Q = _point_add(Q, P)
        P = _point_add(P, P)
        s >>= 1
    return Q


def _point_equal(P, Q):
    if (P[0] * Q[2] - Q[0] * P[2]) % _p != 0:
        return False
    if (P[1] * Q[2] - Q[1] * P[2]) % _p != 0:
        return False
    return True


def _recover_x(y, sign):
    if y >= _p:
        return None
    x2 = (y * y - 1) * pow(_d * y * y + 1, _p - 2, _p)
    if x2 == 0:
        return None if sign else 0
    x = pow(x2, (_p + 3) // 8, _p)
    if (x * x - x2) % _p != 0:
        x = x * _modp_sqrt_m1 % _p
    if (x * x - x2) % _p != 0:
        return None
    if (x & 1) != sign:
        x = _p - x
    return x


_g_y = 4 * pow(5, _p - 2, _p) % _p
_g_x = _recover_x(_g_y, 0)
_G = (_g_x, _g_y, 1, _g_x * _g_y % _p)


def _point_compress(P):
    zinv = pow(P[2], _p - 2, _p)
    x, y = P[0] * zinv % _p, P[1] * zinv % _p
    return int.to_bytes(y | ((x & 1) << 255), 32, "little")


def _point_decompress(s):
    if len(s) != 32:
        raise ValueError("invalid input length for decompression")
    y = int.from_bytes(s, "little")
    sign = y >> 255
    y &= (1 << 255) - 1
    x = _recover_x(y, sign)
    if x is None:
        return None
    return (x, y, 1, x * y % _p)


def _secret_expand(secret):
    h = _sha512(secret)
    a = int.from_bytes(h[:32], "little")
    a &= (1 << 254) - 8
    a |= 1 << 254
    return (a, h[32:])


def _ref_public(secret):
    a, _ = _secret_expand(secret)
    return _point_compress(_point_mul(a, _G))


def _ref_sign(secret, msg):
    a, prefix = _secret_expand(secret)
    A = _point_compress(_point_mul(a, _G))
    r = int.from_bytes(_sha512(prefix + msg), "little") % _q
    Rs = _point_compress(_point_mul(r, _G))
    h = int.from_bytes(_sha512(Rs + A + msg), "little") % _q
    s = (r + h * a) % _q
    return Rs + int.to_bytes(s, 32, "little")


def _ref_verify(public, msg, signature):
    if len(public) != 32 or len(signature) != 64:
        return False
    A = _point_decompress(public)
    if not A:
        return False
    Rs = signature[:32]
    R = _point_decompress(Rs)
    if not R:
        return False
    s = int.from_bytes(signature[32:], "little")
    if s >= _q:
        return False
    h = int.from_bytes(_sha512(Rs + public + msg), "little") % _q
    sB = _point_mul(s, _G)
    hA = _point_mul(h, A)
    return _point_equal(sB, _point_add(R, hA))


# ---- public API ----


def public_key(seed: bytes) -> bytes:
    if BACKEND == "cryptography":
        return Ed25519PrivateKey.from_private_bytes(seed).public_key().public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw
        )
    return _ref_public(seed)


def sign(seed: bytes, msg: bytes) -> bytes:
    if BACKEND == "cryptography":
        return Ed25519PrivateKey.from_private_bytes(seed).sign(msg)
    return _ref_sign(seed, msg)


def verify(public: bytes, msg: bytes, signature: bytes) -> bool:
    if len(public) != 32 or len(signature) != 64:
        return False
    if BACKEND == "cryptography":
        try:
            Ed25519PublicKey.from_public_bytes(public).verify(signature, msg)
            return True
        except (InvalidSignature, ValueError):
            return False
    return _ref_verify(public, msg, signature)
