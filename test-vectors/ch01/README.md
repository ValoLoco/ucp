# Chapter 01 test vectors (reference, TEST ONLY)

Status: **proposal**. These are reference vectors for the chapter 01 reference verifier in [reference/verifier/](../../reference/verifier/). They are not official conformance vectors (chapter 01, Verification method item 1) and they depend on the reference encoding choices (RFC 8785 JCS, SHA-256, Ed25519), which are a **proposal**; the serialization question ([Q-005](../../docs/claims.md)) stays **open**.

All entities, registrations and documents are fictional. All keys are **test only**: they are derived from public strings (see `keys.json`), so anyone can sign with them. Never use them for real records.

## Run

```sh
python3 test-vectors/ch01/run_vectors.py
```

Python 3.10 or newer, no install. Uses the `cryptography` package for Ed25519 when installed, else the bundled RFC 8032 reference code. The runner also checks RFC 8032 test 1, RFC 8785 key ordering, and that `generate.py` reproduces every committed vector byte for byte.

Regenerate after changing the generator: `python3 test-vectors/ch01/generate.py`.

## Fixture format

```json
{
  "testOnly": true,
  "description": "...",
  "record": {},
  "predecessor": {},
  "bundle": [],
  "policy": {},
  "evidence": {},
  "expected": {"status": "valid", "reasonCodes": [], "warnings": []}
}
```

`predecessor`, `bundle`, `policy` and `evidence` are optional. Reason codes are compared as sets.

## Vectors

| File | Expected | Covers |
| --- | --- | --- |
| 01-valid-genesis | valid | genesis, null `previousRecordDigest` |
| 02-valid-successor | valid | successor under predecessor policy, predecessor found by digest |
| 03-bad-signature | invalid `signature-invalid` | field mutated after signing |
| 04-broken-prev-link | invalid `digest-mismatch` | positional predecessor with wrong digest |
| 05-authority-policy-threshold | invalid `signature-missing` | 1 of 2 required signatures |
| 06-authority-policy-unauthorized-signer | invalid `signature-missing` | key listed but not in `authorizedSigners` |
| 07-authority-policy-self-granted | invalid `signature-missing` | successor tries to grant itself a new key |
| 08-malformed-missing-field | invalid `missing-field` | `entityId` missing |
| 09-malformed-type | invalid `field-invalid` | `requiredSignatureCount` 0 |
| 10-indeterminate-anchor | indeterminate `anchor-data-unavailable` | anchor cannot be checked offline |
| 11-anchor-digest-mismatch | invalid `anchor-digest-mismatch` | receipt commits to another digest |
| 12-predecessor-unavailable | indeterminate `predecessor-unavailable` | predecessor withheld |
| 13-competing-successors | indeterminate `competing-successors` | fork in the bundle |
| 14-unsupported-version | invalid `unsupported-protocol-version` | version 9.0.0 |
| 15-experimental-version-allowed | indeterminate `unsupported-protocol-version` | policy allows experimental |
| 16-key-expired | invalid `key-expired` | `validUntil` before `effectiveAt` |
| 17-revocation-data-missing | indeterminate `revocation-data-missing` | `revocationRef`, no material |
| 18-key-revoked | invalid `key-revoked` | material lists the key |
| 19-revocation-not-revoked | valid | material does not list the key |
| 20-registrar-warning | valid, warning | non-blocking registrar policy |
| 21-registrar-blocking | indeterminate | blocking registrar policy |
| 22-valid-genesis-jwk | valid | `publicKeyJwk` key form |
| 23-valid-successor-2-of-2 | valid | threshold met |
| 24-aggregate-invalid-codes | invalid `signature-invalid`, `anchor-digest-mismatch` | step 7 union of invalid codes |
| 25-entity-id-mismatch | invalid `entity-id-mismatch` | successor changes `entityId` |
| 26-unsupported-suite-blocking | indeterminate `unsupported-suite` | only signature under an unsupported suite |
| 27-unsupported-suite-extra | valid, warning `unsupported-suite` | threshold met, extra unsupported signature |
| 28-predecessor-unavailable-anchor-mismatch | invalid `anchor-digest-mismatch` | step 6 still runs after step 2 indeterminate |

Chapter 01 minimal falsification items 1, 2 and 4 are vectors 13, 03 and 12. Item 3 (a complete OpenTimestamps proof reaching valid) cannot be built until an anchoring profile exists; see SPEC-GAPS G-10.
