#!/usr/bin/env python3
"""Run the chapter 01 test vectors against the reference verifier.

Also runs self-checks: RFC 8032 test 1 (Ed25519), RFC 8785 key ordering,
and a regeneration check that committed vectors match generate.py.
Exit code 0 only if everything passes.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "reference" / "verifier"))

from ucp_verifier import ed25519, verify_record  # noqa: E402
from ucp_verifier.canonical import canonicalize  # noqa: E402


def self_checks() -> list[tuple[str, bool]]:
    out = []
    # RFC 8032 section 7.1, TEST 1 (empty message).
    sk = bytes.fromhex("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60")
    pk = bytes.fromhex("d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a")
    sig = bytes.fromhex(
        "e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e06522490155"
        "5fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b"
    )
    out.append(("rfc8032-test1-public-key", ed25519.public_key(sk) == pk))
    out.append(("rfc8032-test1-sign", ed25519.sign(sk, b"") == sig))
    out.append(("rfc8032-test1-verify", ed25519.verify(pk, b"", sig)))
    out.append(("rfc8032-test1-reject-tampered", not ed25519.verify(pk, b"x", sig)))
    # Fallback path, regardless of which backend is active.
    out.append(("rfc8032-reference-fallback", ed25519._ref_verify(pk, b"", sig) and ed25519._ref_sign(sk, b"") == sig))
    # RFC 8785 section 3.2.3 sorting by UTF-16 code units, plus escaping.
    sample = {"\u20ac": 1, "\r": 2, "\ufb33": 3, "1": 4, "\U0001f600": 5, "\u0080": 6, "\u00f6": 7}
    expected = '{"\\r":2,"1":4,"\u0080":6,"\u00f6":7,"\u20ac":1,"\U0001f600":5,"\ufb33":3}'.encode()
    out.append(("rfc8785-key-order", canonicalize(sample) == expected))
    out.append(("rfc8785-literals", canonicalize({"b": [True, False, None], "a": "x\ny"}) == b'{"a":"x\\ny","b":[true,false,null]}'))
    regen = subprocess.run([sys.executable, str(HERE / "generate.py"), "--check"], capture_output=True, text=True)
    out.append(("vectors-regenerate-identically", regen.returncode == 0))
    return out


def main() -> int:
    passed = failed = 0
    print(f"ed25519 backend: {ed25519.BACKEND}")
    for name, ok in self_checks():
        print(f"{'PASS' if ok else 'FAIL'}  self-check {name}")
        passed, failed = passed + ok, failed + (not ok)
    for path in sorted((HERE / "vectors").glob("*.json")):
        vec = json.loads(path.read_text(encoding="utf-8"))
        if vec.get("testOnly") is not True:
            print(f"FAIL  {path.stem}: missing testOnly marker")
            failed += 1
            continue
        res = verify_record(
            vec["record"],
            predecessor=vec.get("predecessor"),
            bundle=vec.get("bundle", []),
            policy=vec.get("policy"),
            evidence=vec.get("evidence"),
        )
        exp = vec["expected"]
        ok = (
            res["status"] == exp["status"]
            and sorted(res["reasonCodes"]) == sorted(exp["reasonCodes"])
            and sorted(res["warnings"]) == sorted(exp.get("warnings", []))
        )
        detail = "" if ok else f"  got {res['status']} {res['reasonCodes']} warnings={res['warnings']}"
        print(f"{'PASS' if ok else 'FAIL'}  {path.stem}: {exp['status']} {exp['reasonCodes']}{detail}")
        passed, failed = passed + ok, failed + (not ok)
    print(f"\n{passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
