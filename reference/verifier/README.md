# UCP chapter 01 reference verifier

Status: **proposal**. Non-normative reference implementation of the seven-step verification sequence in [specs/01-entity-record.md](../../specs/01-entity-record.md). It exists to test whether chapter 01 can be implemented as written and to surface gaps. It is not a conformance authority and makes no claim of cross-vendor wire compatibility (chapter 01, Serialization and digests).

A **valid** result means only that the record passes these checks under this reference's choices. It does not mean legal recognition, registrar confirmation or securities compliance (chapter 01, Trust assumptions).

## What it does

`verify_record(record, predecessor=None, bundle=(), policy=None, evidence=None)` runs the seven steps in order and returns:

```json
{"status": "valid | invalid | indeterminate", "reasonCodes": [], "reasons": [], "warnings": [], "steps": []}
```

| Step | Chapter 01 rule | Reason codes (chapter 03 proposed list) |
| --- | --- | --- |
| 1 Format and protocol version | required fields, types, supported `protocolVersion` | `missing-field`, `field-invalid`, `unsupported-protocol-version` |
| 2 Predecessor and policy | obtain predecessor (positional or by digest from the carried bundle), resolve `authorityPolicy` from it; genesis is self-authorized | `predecessor-unavailable`, `policy-unresolvable` |
| 3 Signatures and keys | Ed25519 signatures, `requiredSignatureCount` of `authorizedSigners`, validity window, carried revocation data | `signature-invalid`, `signature-missing`, `key-expired`, `key-revoked`, `revocation-data-missing`, `unsupported-suite` (indeterminate if the threshold is unmet, else warning), warning `unknown-signer` |
| 4 Sequence and conflicts | `previousRecordDigest` equals predecessor digest, competing successors in the bundle | `digest-mismatch`, `entity-id-mismatch`, `competing-successors` |
| 5 Registration evidence | never treated as legal recognition; registrar confirmation per policy | `registrar-confirmation-unavailable` (warning by default) |
| 6 Anchor receipt | skip if absent; digest commitment check; otherwise indeterminate offline | `anchor-proof-invalid`, `anchor-digest-mismatch`, `anchor-data-unavailable` |
| 7 Report | union of invalid codes, else union of blocking indeterminate codes, else valid with warnings | |

All codes are from the chapter 03 proposed list. Steps record results and continue; only a step 1 failure stops verification, and a step 2 indeterminate skips steps 3 and 4 (chapter 01 evaluation order). Remaining open items are in [SPEC-GAPS.md](SPEC-GAPS.md).

Offline only: no network calls of any kind. The verifier never contacts Bitcoin nodes, OpenTimestamps calendars, DID resolvers or registrars. Where chapter 01 needs data it does not have, it returns **indeterminate**.

## Reference choices (all proposal, not normative)

Chapter 01 leaves the encoding open ([Q-005](../../docs/claims.md), chapter 01 open question 5). This reference does **not** change that status. To make the steps testable it picks:

- **Canonicalization: RFC 8785 JCS** over the JSON record, restricted to strings, integers, booleans, null, arrays and objects (non-integer numbers are rejected). Why JCS for the reference: chapter 01 examples and fields are already JSON, JCS needs no schema or tag registry, the test vectors stay human-readable and diffable, and it can be implemented in about 60 lines with the standard library. Deterministic CBOR (RFC 8949 section 4.2) would give smaller, binary-safe signing inputs and remains a candidate; the choice for UCP stays an **open question**.
- **Signing payload:** JCS of the record without `signatures` and `anchorReceipt` (chapter 01 `signatures` row).
- **Record digest:** `sha256:` plus lowercase hex SHA-256 of JCS of the record without `anchorReceipt`, signatures included (chapter 01 Record digest, proposal; only the JCS part is reference-specific).
- **Suite name** `ucp-ref-ed25519-jcs-sha256-2026`: Ed25519 (RFC 8032) over the payload bytes, signature as unpadded base64url.
- **Keys:** `publicKeyMultibase` as base58btc Ed25519 multikey (`z` + base58(0xed01 + key)) or `publicKeyJwk` as OKP/Ed25519. Exactly one per key (chapter 01 Key encodings).
- **Ed25519 library:** the `cryptography` package when installed, else the RFC 8032 section 6 reference algorithm bundled in `ed25519.py` (slow, not constant-time, fine for tests). Both paths pass RFC 8032 test 1.

## Run

Requires Python 3.10 or newer. No install step.

```sh
python3 test-vectors/ch01/run_vectors.py             # all vectors and self-checks
cd reference/verifier && python3 -m ucp_verifier ../../test-vectors/ch01/vectors/02-valid-successor.json
```

Exit code of the CLI: 0 valid, 1 invalid, 3 indeterminate.

## Policy and evidence inputs (reference only)

`policy` keys: `allowExperimentalVersions`, `requireRegistrarConfirmation`, `registrarConfirmationBlocking` (all default false). `evidence.revocations` maps a `revocationRef` to `{"revokedKeyIds": [...]}`. The policy key names match chapter 01 step 5 and chapter 03 required inputs; the revocation shape is not specified by any chapter (chapter 01 open question 10).

## Scope limits

- One record per call, as chapter 01 defines. The predecessor is used for policy and digest checks but is not itself re-verified; full history verification is chapter 03 and out of scope here.
- `delegationPolicy`, `recoveryPolicy` and DID migration rules are shape-checked only, not evaluated.
- No anchoring profile is implemented, so a record with `anchorReceipt` can never reach **valid** in this reference.

License: the root README proposes MIT for code; final licensing is still open per [CONTRIBUTING.md](../../CONTRIBUTING.md).
