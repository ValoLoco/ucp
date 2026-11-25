"""Small encoders: base58btc multibase Ed25519 multikey, base64url."""

from __future__ import annotations

import base64

_B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
ED25519_PUB_MULTICODEC = b"\xed\x01"


def b58encode(data: bytes) -> str:
    n = int.from_bytes(data, "big")
    out = ""
    while n:
        n, r = divmod(n, 58)
        out = _B58[r] + out
    pad = len(data) - len(data.lstrip(b"\x00"))
    return "1" * pad + out


def b58decode(s: str) -> bytes:
    n = 0
    for ch in s:
        idx = _B58.find(ch)
        if idx < 0:
            raise ValueError("invalid base58 character")
        n = n * 58 + idx
    body = n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b""
    pad = len(s) - len(s.lstrip("1"))
    return b"\x00" * pad + body


def ed25519_multikey(pub: bytes) -> str:
    return "z" + b58encode(ED25519_PUB_MULTICODEC + pub)


def decode_ed25519_multikey(value: str) -> bytes:
    if not value.startswith("z"):
        raise ValueError("only base58btc multibase ('z') is supported")
    raw = b58decode(value[1:])
    if not raw.startswith(ED25519_PUB_MULTICODEC) or len(raw) != 34:
        raise ValueError("not an Ed25519 multikey")
    return raw[2:]


def decode_ed25519_jwk(jwk) -> bytes:
    if not isinstance(jwk, dict) or jwk.get("kty") != "OKP" or jwk.get("crv") != "Ed25519":
        raise ValueError("only OKP Ed25519 JWKs are supported")
    raw = b64url_decode(jwk.get("x", ""))
    if len(raw) != 32:
        raise ValueError("bad Ed25519 JWK x length")
    return raw


def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def b64url_decode(s: str) -> bytes:
    if not isinstance(s, str) or "=" in s:
        raise ValueError("expected unpadded base64url")
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))
