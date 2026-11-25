#!/usr/bin/env python3
"""Generate the chapter 01 test vectors deterministically.

TEST ONLY. All keys are derived from public seeds:
seed = SHA-256("UCP-TEST-VECTOR-ONLY-NOT-A-REAL-KEY:" + name).
Anyone can recompute these private keys. Never use them for anything real.

Usage:
  python3 generate.py          # (re)write vectors/*.json and keys.json
  python3 generate.py --check  # fail if committed files differ
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "reference" / "verifier"))

from ucp_verifier import REFERENCE_SUITE, record_digest, signing_payload  # noqa: E402
from ucp_verifier import ed25519  # noqa: E402
from ucp_verifier.encoding import b64url_encode, ed25519_multikey  # noqa: E402

SEED_PREFIX = b"UCP-TEST-VECTOR-ONLY-NOT-A-REAL-KEY:"
KEY_NAMES = ("test-key-a", "test-key-b", "test-key-c")
ENTITY = "ucp:entity:test-vector-only-fictional-entity"


def seed(name: str) -> bytes:
    return hashlib.sha256(SEED_PREFIX + name.encode()).digest()


PUB = {n: ed25519_multikey(ed25519.public_key(seed(n))) for n in KEY_NAMES}


def key(name: str, **extra) -> dict:
    k = {"id": name, "publicKeyMultibase": PUB[name], "role": "administrator", "validFrom": "2026-01-01T00:00:00Z"}
    k.update(extra)
    return k


def sign(record: dict, *signers: str) -> dict:
    r = copy.deepcopy(record)
    payload = signing_payload(r)
    r["signatures"] = [
        {"keyId": s, "suite": REFERENCE_SUITE, "signature": b64url_encode(ed25519.sign(seed(s), payload))}
        for s in signers
    ]
    return r


def base_genesis(**over) -> dict:
    r = {
        "protocolVersion": "0.1.0",
        "entityId": ENTITY,
        "legalRegistrations": [
            {"jurisdiction": "EX-FICT", "officialId": "FICT-TEST-0001", "evidence": ["sha256:" + "00" * 32]}
        ],
        "authorizedKeys": [key("test-key-a"), key("test-key-b")],
        "authorityPolicy": {"authorizedSigners": ["test-key-a"], "requiredSignatureCount": 1},
        "documents": [{"label": "Fictional operating agreement", "digest": "sha256:" + "11" * 32}],
        "previousRecordDigest": None,
        "effectiveAt": "2026-06-15T12:00:00Z",
        "signatures": [],
        "anchorReceipt": None,
    }
    r.update(over)
    return r


def successor(prev: dict, **over) -> dict:
    r = copy.deepcopy(prev)
    r["previousRecordDigest"] = record_digest(prev)
    r["effectiveAt"] = "2026-07-01T12:00:00Z"
    r["documents"] = r["documents"] + [{"label": "Fictional amendment", "digest": "sha256:" + "22" * 32}]
    r["signatures"] = []
    r["anchorReceipt"] = None
    r.update(over)
    return r


def build() -> dict[str, dict]:
    v: dict[str, dict] = {}
    g = sign(base_genesis(), "test-key-a")

    def add(name, desc, record, expected_status, codes=(), warnings=(), **inputs):
        v[name] = {
            "testOnly": True,
            "description": desc,
            "record": record,
            **inputs,
            "expected": {"status": expected_status, "reasonCodes": list(codes), "warnings": list(warnings)},
        }

    add("01-valid-genesis", "Genesis record, null previousRecordDigest, one required signature.", g, "valid")

    s = sign(successor(g), "test-key-a")
    add("02-valid-successor", "Successor signed under the predecessor's authorityPolicy; predecessor found in bundle by digest.",
        s, "valid", bundle=[g])

    tampered = copy.deepcopy(g)
    tampered["entityId"] = ENTITY + "-tampered"
    add("03-bad-signature", "Signed field mutated after signing (ch01 minimal falsification item 2).",
        tampered, "invalid", ["signature-invalid"])

    other = sign(base_genesis(effectiveAt="2026-05-01T00:00:00Z"), "test-key-a")
    broken = sign(successor(g), "test-key-a")
    add("04-broken-prev-link", "Predecessor supplied positionally, but previousRecordDigest does not match its digest.",
        broken, "invalid", ["digest-mismatch"], predecessor=other)

    g2 = sign(base_genesis(authorityPolicy={"authorizedSigners": ["test-key-a", "test-key-b"], "requiredSignatureCount": 2}),
              "test-key-a", "test-key-b")
    s2 = sign(successor(g2), "test-key-a")
    add("05-authority-policy-threshold", "Predecessor policy requires 2 signatures; successor carries 1.",
        s2, "invalid", ["signature-missing"], bundle=[g2])

    s3 = sign(successor(g), "test-key-b")
    add("06-authority-policy-unauthorized-signer", "Successor signed only by test-key-b, which is an authorized key but not in authorizedSigners.",
        s3, "invalid", ["signature-missing"], bundle=[g])

    s4 = sign(successor(g, authorityPolicy={"authorizedSigners": ["test-key-c"], "requiredSignatureCount": 1},
                        authorizedKeys=[key("test-key-c")]), "test-key-c")
    add("07-authority-policy-self-granted", "Successor replaces keys with test-key-c and signs only with it; the predecessor policy does not authorize test-key-c.",
        s4, "invalid", ["signature-missing"], ["x-ref-unknown-signer"], bundle=[g])

    m = copy.deepcopy(g)
    del m["entityId"]
    add("08-malformed-missing-field", "Required field entityId missing.", m, "invalid", ["missing-field"])

    m2 = sign(base_genesis(authorityPolicy={"authorizedSigners": ["test-key-a"], "requiredSignatureCount": 0}), "test-key-a")
    add("09-malformed-type", "requiredSignatureCount is not a positive integer.", m2, "invalid", ["x-ref-field-invalid"])

    anchored = sign(base_genesis(), "test-key-a")
    anchored["anchorReceipt"] = {"profile": "opentimestamps", "recordDigest": record_digest(anchored), "proof": "VEVTVC1PTkxZ"}
    add("10-indeterminate-anchor", "OpenTimestamps-named receipt committing to the right digest; no profile is specified and no chain data is carried, so it cannot be checked offline.",
        anchored, "indeterminate", ["anchor-data-unavailable"])

    wrong_anchor = copy.deepcopy(anchored)
    wrong_anchor["anchorReceipt"]["recordDigest"] = "sha256:" + "33" * 32
    add("11-anchor-digest-mismatch", "anchorReceipt commits to a digest other than the record digest.",
        wrong_anchor, "invalid", ["anchor-digest-mismatch"])

    add("12-predecessor-unavailable", "Successor without its predecessor (ch01 minimal falsification item 4).",
        s, "indeterminate", ["predecessor-unavailable"])

    rival = sign(successor(g, documents=g["documents"] + [{"label": "Fictional rival amendment", "digest": "sha256:" + "44" * 32}]), "test-key-a")
    add("13-competing-successors", "Two signed successors share one previousRecordDigest (ch01 minimal falsification item 1).",
        s, "indeterminate", ["competing-successors"], bundle=[g, rival])

    v9 = sign(base_genesis(protocolVersion="9.0.0"), "test-key-a")
    add("14-unsupported-version", "protocolVersion 9.0.0 is not supported.", v9, "invalid", ["unsupported-protocol-version"])
    add("15-experimental-version-allowed", "Same record; local policy allows experimental versions.",
        v9, "indeterminate", ["unsupported-protocol-version"], policy={"allowExperimentalVersions": True})

    exp = sign(base_genesis(authorizedKeys=[key("test-key-a", validUntil="2026-03-01T00:00:00Z"), key("test-key-b")]), "test-key-a")
    add("16-key-expired", "Signing key validUntil is before effectiveAt.", exp, "invalid", ["key-expired"])

    rev = sign(base_genesis(authorizedKeys=[key("test-key-a", revocationRef="urn:test:revocation-list-1"), key("test-key-b")]), "test-key-a")
    add("17-revocation-data-missing", "Signing key has revocationRef but no revocation material is carried.",
        rev, "indeterminate", ["revocation-data-missing"])
    add("18-key-revoked", "Carried revocation material lists the signing key.",
        rev, "invalid", ["key-revoked"], evidence={"revocations": {"urn:test:revocation-list-1": {"revokedKeyIds": ["test-key-a"]}}})
    add("19-revocation-not-revoked", "Carried revocation material does not list the signing key.",
        rev, "valid", evidence={"revocations": {"urn:test:revocation-list-1": {"revokedKeyIds": []}}})

    add("20-registrar-warning", "Policy wants registrar confirmation, non-blocking: valid with warning.",
        g, "valid", warnings=["registrar-confirmation-unavailable"], policy={"requireRegistrarConfirmation": True})
    add("21-registrar-blocking", "Policy wants registrar confirmation and treats it as blocking.",
        g, "indeterminate", ["registrar-confirmation-unavailable"],
        policy={"requireRegistrarConfirmation": True, "registrarConfirmationBlocking": True})

    jwk_key = {"id": "test-key-a", "publicKeyJwk": {"kty": "OKP", "crv": "Ed25519",
               "x": b64url_encode(ed25519.public_key(seed("test-key-a")))}, "role": "administrator"}
    gj = sign(base_genesis(authorizedKeys=[jwk_key]), "test-key-a")
    add("22-valid-genesis-jwk", "Genesis using publicKeyJwk instead of publicKeyMultibase.", gj, "valid")

    s5 = sign(successor(g2), "test-key-a", "test-key-b")
    add("23-valid-successor-2-of-2", "Successor meets a 2-of-2 predecessor policy.", s5, "valid", bundle=[g2])
    return v


def keys_doc() -> dict:
    return {
        "testOnly": True,
        "warning": "TEST ONLY. These private keys are derived from public strings and are known to everyone. Never use them for real records.",
        "derivation": "seed = SHA-256('UCP-TEST-VECTOR-ONLY-NOT-A-REAL-KEY:' + name); Ed25519 private key = seed (RFC 8032)",
        "keys": [{"name": n, "seedHex": seed(n).hex(), "publicKeyMultibase": PUB[n]} for n in KEY_NAMES],
    }


def render(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def main(argv) -> int:
    check = "--check" in argv
    files = {HERE / "keys.json": render(keys_doc())}
    for name, vec in build().items():
        files[HERE / "vectors" / f"{name}.json"] = render(vec)
    if check:
        bad = [p for p, c in files.items() if not p.is_file() or p.read_text(encoding="utf-8") != c]
        existing = set((HERE / "vectors").glob("*.json"))
        extra = existing - set(files)
        for p in bad:
            print(f"DIFFERS: {p.relative_to(HERE)}")
        for p in sorted(extra):
            print(f"UNEXPECTED: {p.relative_to(HERE)}")
        return 1 if bad or extra else 0
    (HERE / "vectors").mkdir(exist_ok=True)
    for p, c in files.items():
        p.write_text(c, encoding="utf-8")
    print(f"wrote {len(files) - 1} vectors and keys.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
