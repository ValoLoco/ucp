"""Chapter 01 seven-step verifier, reference implementation.

Every step follows specs/01-entity-record.md, "Seven-step verification
sequence (normative)", including its evaluation order (steps record
results; only steps 1 and 2 stop later steps) and the step 7 aggregation
shared with chapter 03 Phase E. Reason codes come from the proposed list
in specs/03-verification.md. Open items are tracked in SPEC-GAPS.md.

Reference choices (Proposal, not normative):
- signing payload: RFC 8785 JCS of the record without `signatures` and
  `anchorReceipt`;
- record digest: `sha256:` + hex SHA-256 of JCS of the record without
  `anchorReceipt` (signatures included), as chapter 01 "Record digest"
  proposes; JCS itself is still open (Q-005);
- signature suite `ucp-ref-ed25519-jcs-sha256-2026`: Ed25519 over the
  signing payload bytes, signature as unpadded base64url.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import re
from typing import Any, Iterable

from . import ed25519
from .canonical import CanonicalizationError, canonicalize
from .encoding import b64url_decode, decode_ed25519_jwk, decode_ed25519_multikey

SUPPORTED_PROTOCOL_VERSIONS = frozenset({"0.1.0"})
REFERENCE_SUITE = "ucp-ref-ed25519-jcs-sha256-2026"

DEFAULT_POLICY = {
    "allowExperimentalVersions": False,
    "requireRegistrarConfirmation": False,
    "registrarConfirmationBlocking": False,
}

SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)
RFC3339_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})$"
)

REQUIRED_FIELDS = (
    "protocolVersion",
    "entityId",
    "legalRegistrations",
    "authorizedKeys",
    "authorityPolicy",
    "documents",
    "previousRecordDigest",
    "effectiveAt",
    "signatures",
)


# ---------------------------------------------------------------- helpers


def _strip(record: dict, *names: str) -> dict:
    return {k: v for k, v in record.items() if k not in names}


def signing_payload(record: dict) -> bytes:
    return canonicalize(_strip(record, "signatures", "anchorReceipt"))


def record_digest(record: dict) -> str:
    return "sha256:" + hashlib.sha256(canonicalize(_strip(record, "anchorReceipt"))).hexdigest()


def parse_rfc3339(value: Any) -> dt.datetime | None:
    if not isinstance(value, str) or not RFC3339_RE.match(value):
        return None
    try:
        return dt.datetime.fromisoformat(value.upper().replace("Z", "+00:00"))
    except ValueError:
        return None


def _is_str(v: Any, nonempty: bool = True) -> bool:
    return isinstance(v, str) and (bool(v) or not nonempty)


def _is_int(v: Any) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def key_bytes(key: dict) -> bytes:
    if "publicKeyMultibase" in key:
        return decode_ed25519_multikey(key["publicKeyMultibase"])
    return decode_ed25519_jwk(key["publicKeyJwk"])


class _Step:
    def __init__(self, number: int, name: str):
        self.number = number
        self.name = name
        self.outcome = "pass"
        self.codes: list[str] = []
        self.reasons: list[str] = []
        self.warnings: list[str] = []

    def fail(self, outcome: str, code: str, reason: str) -> None:
        rank = {"pass": 0, "indeterminate": 1, "invalid": 2}
        if rank[outcome] > rank[self.outcome]:
            self.outcome = outcome
        if code not in self.codes:
            self.codes.append(code)
        self.reasons.append(reason)

    def warn(self, code: str, reason: str) -> None:
        if code not in self.warnings:
            self.warnings.append(code)
        self.reasons.append(reason)

    def as_dict(self) -> dict:
        return {
            "step": self.number,
            "name": self.name,
            "outcome": self.outcome,
            "codes": self.codes,
            "warnings": self.warnings,
        }


# ---------------------------------------------------------------- step 1


def structural_problems(record: Any) -> list[tuple[str, str]]:
    """Return (code, reason) pairs for missing fields and type violations."""
    if not isinstance(record, dict):
        return [("field-invalid", "record is not a JSON object")]
    out: list[tuple[str, str]] = []
    for name in REQUIRED_FIELDS:
        if name not in record:
            out.append(("missing-field", f"missing required field {name}"))
    if out:
        return out

    def bad(reason: str) -> None:
        out.append(("field-invalid", reason))

    if not _is_str(record["protocolVersion"]) or not SEMVER_RE.match(record["protocolVersion"]):
        bad("protocolVersion is not a semantic version string")
    if not _is_str(record["entityId"]):
        bad("entityId must be a non-empty string")

    regs = record["legalRegistrations"]
    if not isinstance(regs, list):
        bad("legalRegistrations must be an array")
    else:
        for i, reg in enumerate(regs):
            if not isinstance(reg, dict) or not _is_str(reg.get("jurisdiction")):
                bad(f"legalRegistrations[{i}] needs a jurisdiction string")
                continue
            if "officialId" in reg and not _is_str(reg["officialId"]):
                bad(f"legalRegistrations[{i}].officialId must be a string")
            if "evidence" in reg and (
                not isinstance(reg["evidence"], list) or not all(_is_str(e) for e in reg["evidence"])
            ):
                bad(f"legalRegistrations[{i}].evidence must be an array of strings")

    keys = record["authorizedKeys"]
    key_ids: set[str] = set()
    if not isinstance(keys, list) or not keys:
        bad("authorizedKeys must be a non-empty array")
    else:
        for i, key in enumerate(keys):
            if not isinstance(key, dict):
                bad(f"authorizedKeys[{i}] must be an object")
                continue
            if not _is_str(key.get("id")):
                bad(f"authorizedKeys[{i}].id must be a non-empty string")
            elif key["id"] in key_ids:
                bad(f"authorizedKeys id {key['id']} is duplicated")
            else:
                key_ids.add(key["id"])
            if not _is_str(key.get("role")):
                bad(f"authorizedKeys[{i}].role must be a non-empty string")
            has_mb, has_jwk = "publicKeyMultibase" in key, "publicKeyJwk" in key
            if has_mb == has_jwk:
                bad(f"authorizedKeys[{i}] needs exactly one of publicKeyMultibase or publicKeyJwk")
            else:
                try:
                    key_bytes(key)
                except (ValueError, TypeError, AttributeError):
                    bad(f"authorizedKeys[{i}] public key is not a decodable Ed25519 key")
            for f in ("validFrom", "validUntil"):
                if f in key and parse_rfc3339(key[f]) is None:
                    bad(f"authorizedKeys[{i}].{f} is not RFC 3339")
            if "revocationRef" in key and not _is_str(key["revocationRef"]):
                bad(f"authorizedKeys[{i}].revocationRef must be a string")

    pol = record["authorityPolicy"]
    if not isinstance(pol, dict):
        bad("authorityPolicy must be an object")
    else:
        signers = pol.get("authorizedSigners")
        if not isinstance(signers, list) or not signers or not all(_is_str(s) for s in signers):
            bad("authorityPolicy.authorizedSigners must be a non-empty array of key ids")
        else:
            for s in signers:
                if s not in key_ids:
                    bad(f"authorityPolicy.authorizedSigners entry {s} is not an authorizedKeys id")
        count = pol.get("requiredSignatureCount")
        if not _is_int(count) or count < 1:
            bad("authorityPolicy.requiredSignatureCount must be a positive integer")
        elif isinstance(signers, list) and count > len(set(signers)):
            bad("authorityPolicy.requiredSignatureCount exceeds the number of authorizedSigners")
        if "recoveryPolicy" in pol and not isinstance(pol["recoveryPolicy"], dict):
            bad("authorityPolicy.recoveryPolicy must be an object")
        if "delegationPolicy" in pol and (
            not isinstance(pol["delegationPolicy"], list)
            or not all(isinstance(d, dict) for d in pol["delegationPolicy"])
        ):
            bad("authorityPolicy.delegationPolicy must be an array of delegation objects")

    docs = record["documents"]
    if not isinstance(docs, list):
        bad("documents must be an array")
    else:
        for i, doc in enumerate(docs):
            if not isinstance(doc, dict) or not _is_str(doc.get("digest")):
                bad(f"documents[{i}] needs a digest string")

    prev = record["previousRecordDigest"]
    if prev is not None and not _is_str(prev):
        bad("previousRecordDigest must be a string or null")

    if parse_rfc3339(record["effectiveAt"]) is None:
        bad("effectiveAt is not RFC 3339")

    sigs = record["signatures"]
    if not isinstance(sigs, list) or not sigs:
        bad("signatures must be a non-empty array")
    else:
        for i, sig in enumerate(sigs):
            if not isinstance(sig, dict) or not all(
                _is_str(sig.get(f)) for f in ("keyId", "signature", "suite")
            ):
                bad(f"signatures[{i}] needs keyId, signature and suite strings")

    if record.get("anchorReceipt") is not None and not isinstance(record["anchorReceipt"], dict):
        bad("anchorReceipt must be an object or null")

    if not out:
        try:
            canonicalize(record)
        except CanonicalizationError as exc:
            out.append(("field-invalid", f"record cannot be canonicalized: {exc}"))
    return out


# ---------------------------------------------------------------- main


def verify_record(
    record: Any,
    predecessor: dict | None = None,
    bundle: Iterable[dict] = (),
    policy: dict | None = None,
    evidence: dict | None = None,
) -> dict:
    """Run the chapter 01 seven-step sequence on one record.

    predecessor: the prior record when supplied positionally (as in a ch03
        tip chain). If omitted, the predecessor is looked up in `bundle` by
        digest.
    bundle: other carried records (predecessor candidates, possible
        competing successors).
    policy: verifier policy, see DEFAULT_POLICY.
    evidence: carried offline proofs, currently `revocations`
        ({revocationRef: {"revokedKeyIds": [...]}}).
    """
    pol = {**DEFAULT_POLICY, **(policy or {})}
    ev = evidence or {}
    bundle = [r for r in bundle if isinstance(r, dict)]
    steps: list[_Step] = []

    def finish() -> dict:
        reason_codes: list[str] = []
        warnings: list[str] = []
        reasons: list[str] = []
        status = "valid"
        for s in steps:
            reasons.extend(s.reasons)
            for w in s.warnings:
                if w not in warnings:
                    warnings.append(w)
            if s.outcome == "invalid":
                status = "invalid"
        if status != "invalid" and any(s.outcome == "indeterminate" for s in steps):
            status = "indeterminate"
        for s in steps:
            if (status == "invalid" and s.outcome == "invalid") or (
                status == "indeterminate" and s.outcome == "indeterminate"
            ):
                for c in s.codes:
                    if c not in reason_codes:
                        reason_codes.append(c)
        return {
            "status": status,
            "reasonCodes": reason_codes,
            "reasons": reasons,
            "warnings": warnings,
            "steps": [s.as_dict() for s in steps],
        }

    # Step 1: format and protocol version.
    s1 = _Step(1, "format-and-protocol-version")
    steps.append(s1)
    for code, reason in structural_problems(record):
        s1.fail("invalid", code, reason)
    if s1.outcome != "pass":
        return finish()
    if record["protocolVersion"] not in SUPPORTED_PROTOCOL_VERSIONS:
        if pol["allowExperimentalVersions"]:
            s1.fail("indeterminate", "unsupported-protocol-version", "unsupported protocolVersion")
        else:
            s1.fail("invalid", "unsupported-protocol-version", "unsupported protocolVersion")
        return finish()

    # Step 2: predecessor and policy.
    s2 = _Step(2, "predecessor-and-policy")
    steps.append(s2)
    prev_digest = record["previousRecordDigest"]
    context: dict | None
    if prev_digest is None:
        context = record  # genesis is self-authorized (ch01 step 2)
    else:
        # Positional predecessor first, else lookup by digest (ch01 step 2).
        pred = predecessor
        if pred is None:
            pred = next((r for r in bundle if _safe_digest(r) == prev_digest), None)
        if pred is None:
            s2.fail("indeterminate", "predecessor-unavailable", "predecessor unavailable")
            context = None
        elif structural_problems(pred):
            s2.fail("indeterminate", "policy-unresolvable", "authorityPolicy cannot be resolved from predecessor")
            context = None
        else:
            predecessor = pred
            context = pred
    if context is not None:
        _signatures_and_sequence(record, context, predecessor, bundle, ev, steps)
    _evidence_and_anchor(record, pol, steps)
    steps.append(_Step(7, "report"))
    return finish()


def _signatures_and_sequence(record: dict, context: dict, predecessor: dict | None,
                             bundle: list, ev: dict, steps: list) -> None:
    """Steps 3 and 4. Skipped by the caller when step 2 is indeterminate."""
    prev_digest = record["previousRecordDigest"]
    ctx_keys = {k["id"]: k for k in context["authorizedKeys"]}
    ctx_policy = context["authorityPolicy"]

    # Step 3: signatures and keys.
    s3 = _Step(3, "signatures-and-keys")
    steps.append(s3)
    payload = signing_payload(record)
    effective = parse_rfc3339(record["effectiveAt"])
    signers = set(ctx_policy["authorizedSigners"])
    counted: set[str] = set()
    unsupported: list[str] = []
    for sig in record["signatures"]:
        if sig["suite"] != REFERENCE_SUITE:
            unsupported.append(sig["suite"])
            continue
        key = ctx_keys.get(sig["keyId"])
        if key is None:
            s3.warn("unknown-signer", f"signature by {sig['keyId']} is not from an authorized key; ignored")
            continue
        try:
            raw_sig = b64url_decode(sig["signature"])
        except (ValueError, TypeError):
            raw_sig = b""
        if not ed25519.verify(key_bytes(key), payload, raw_sig):
            s3.fail("invalid", "signature-invalid", f"signature by {sig['keyId']} does not verify")
            continue
        if sig["keyId"] not in signers:
            continue
        vf, vu = parse_rfc3339(key.get("validFrom")), parse_rfc3339(key.get("validUntil"))
        if (vf and effective < vf) or (vu and effective > vu):
            s3.fail("invalid", "key-expired", f"key {sig['keyId']} is outside its validity window at effectiveAt")
            continue
        if "revocationRef" in key:
            material = (ev.get("revocations") or {}).get(key["revocationRef"])
            if not isinstance(material, dict):
                s3.fail("indeterminate", "revocation-data-missing", f"no revocation data for key {sig['keyId']}")
                continue
            if sig["keyId"] in (material.get("revokedKeyIds") or []):
                s3.fail("invalid", "key-revoked", f"key {sig['keyId']} is revoked")
                continue
        counted.add(sig["keyId"])
    required = ctx_policy["requiredSignatureCount"]
    if unsupported and len(counted) >= required:
        s3.warn("unsupported-suite", f"uncounted signatures under unsupported suites: {sorted(set(unsupported))}")
    elif s3.outcome == "pass" and len(counted) < required:
        if unsupported:
            s3.fail("indeterminate", "unsupported-suite",
                    f"{len(counted)} of {required} required signatures verified; others use unsupported suites")
        else:
            s3.fail("invalid", "signature-missing", f"{len(counted)} of {required} required signatures present")

    # Step 4: sequence and conflicts.
    s4 = _Step(4, "sequence-and-conflicts")
    steps.append(s4)
    if prev_digest is not None:
        if record_digest(predecessor) != prev_digest:
            s4.fail("invalid", "digest-mismatch", "previousRecordDigest does not match predecessor digest")
        elif predecessor["entityId"] != record["entityId"]:
            s4.fail("invalid", "entity-id-mismatch", "entityId differs from predecessor")
        else:
            own = record_digest(record)
            rivals = [
                r
                for r in bundle
                if r.get("previousRecordDigest") == prev_digest
                and r.get("entityId") == record["entityId"]
                and _safe_digest(r) not in (None, own)
            ]
            if rivals:
                s4.fail("indeterminate", "competing-successors", "competing successors")


def _evidence_and_anchor(record: dict, pol: dict, steps: list) -> None:
    """Steps 5 and 6. They run even when earlier steps failed (ch01 step 7)."""
    # Step 5: registration evidence. Presence is never legal recognition.
    s5 = _Step(5, "registration-evidence")
    steps.append(s5)
    if pol["requireRegistrarConfirmation"]:
        # No offline registrar evidence format exists yet (ch01 open question 13),
        # so confirmation is never available here. Non-blocking unless policy
        # sets registrarConfirmationBlocking (ch01 step 5, ch03 Phase A).
        if pol["registrarConfirmationBlocking"]:
            s5.fail("indeterminate", "registrar-confirmation-unavailable", "registrar confirmation unavailable offline")
        else:
            s5.warn("registrar-confirmation-unavailable", "registrar confirmation unavailable offline")

    # Step 6: anchor receipt.
    s6 = _Step(6, "anchor-receipt")
    steps.append(s6)
    receipt = record.get("anchorReceipt")
    if receipt is not None:
        if not _is_str(receipt.get("profile")):
            s6.fail("invalid", "anchor-proof-invalid", "anchorReceipt does not name an anchoring profile")
        elif "recordDigest" in receipt and receipt["recordDigest"] != record_digest(record):
            s6.fail("invalid", "anchor-digest-mismatch", "anchorReceipt commits to a different digest")
        else:
            # No anchoring profile is specified yet and this reference never
            # contacts the Bitcoin network, so the commitment cannot be
            # checked offline (SPEC-GAPS G-10, G-11).
            s6.fail(
                "indeterminate",
                "anchor-data-unavailable",
                f"anchor profile {receipt['profile']} cannot be verified offline by this reference",
            )


def _safe_digest(r: Any) -> str | None:
    try:
        return record_digest(r)
    except (CanonicalizationError, AttributeError, TypeError):
        return None
