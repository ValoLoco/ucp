# UCP Core v0.1

Status: discussion draft. Not an interoperability standard or production implementation. Claim labels: [00-conventions.md](00-conventions.md). Cited facts: [docs/claims.md](../docs/claims.md).

## Purpose

Describe a portable entity record whose claims, authority, and history can be independently examined without implying legal recognition.

## Minimum record

- protocolVersion: format version.
- entityId: protocol identifier, distinct from any official registration number.
- legalRegistrations: claimed jurisdictions, official identifiers, and evidence references.
- authorizedKeys: public keys, roles, validity periods, and revocation references.
- authorityPolicy: who may authorize updates and how recovery works.
- documents: references and digests for governing documents.
- previousRecordDigest: link to the preceding accepted record.
- effectiveAt: claimed effective time, not a trusted timestamp.
- signatures: authorizations over the record using a specified signing profile.
- anchorReceipt: optional external commitment proof.

Personal information, identity documents, and confidential contracts stay outside public records and public anchors.

## Verification sequence

1. Validate the record format and protocol version.
2. Resolve the preceding record and authority policy.
3. Verify signatures and key validity under the selected profile.
4. Check revocations, update sequence, and conflicting records.
5. Inspect registration evidence without treating its presence as legal recognition.
6. Verify any anchor receipt and its confirmation assumptions.
7. Report valid, invalid, or indeterminate with explicit reasons.

## Decisions still required

Canonical serialization, digest algorithm, signature suite, identifier generation, fork resolution, recovery, revocation freshness, and anchoring format must be selected and tested before interoperability claims.

## Explicit exclusions

No securities issuance, autonomous legal personality, universal court, compulsory reputation score, or interplanetary consensus in this version.
