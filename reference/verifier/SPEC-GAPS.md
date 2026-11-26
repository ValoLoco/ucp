# Chapter 01 spec gaps found while implementing

Status after the spec gap fix pass: 13 gaps are closed by **proposal** text in the spec (some resting on sourced facts), 5 are partly closed with the remainder kept as an **open question**, and 3 stay **open questions**. "Closed" means the spec now states a rule the reference verifier implements; a proposal is still not normative consensus. Section references are to [specs/01-entity-record.md](../../specs/01-entity-record.md) unless noted.

| Id | Gap (short) | Status | Where it is addressed | Label |
| --- | --- | --- | --- | --- |
| G-01 | Canonical serialization unset (Q-005). | Open | Serialization and digests; open question 5. The reference keeps RFC 8785 JCS as a labeled proposal. | Open question |
| G-02 | Digest algorithm, encoding and input undefined. | Closed | Record digest: SHA-256 (FIPS 180-4, RFC 6234, C-047), `sha256:` + lowercase hex, record without `anchorReceipt`, signatures included. Byte input still depends on G-01. | Proposal (algorithm sourced) |
| G-03 | Which policy authorizes a genesis record. | Closed | Step 2, genesis bullet: self-authorized, self-asserted only. | Proposal |
| G-04 | Policy replacement "per local rules". | Closed | Step 2, policy changes bullet: changes authorized by the predecessor only, effective from the next record. `recoveryPolicy` evaluation stays undefined. | Proposal |
| G-05 | Which keys count; unknown or unlisted signers. | Closed | Step 3, which keys count bullet; reason code `unknown-signer` added to chapter 03. | Proposal |
| G-06 | Validity window has no trusted reference time. | Partly closed | Step 3, validity window bullet: `effectiveAt` outside the window is invalid (self-contradiction). Which trusted time to use stays open question 9 (Q-032) with options. | Proposal + Open question |
| G-07 | Revocation format, freshness and "definitive" test. | Partly closed | Step 3, definitive revocation bullet (fresh carried material, aligned with chapter 03 Phase C). Format stays open question 10 (Q-033). The reference does not evaluate staleness because its material has no issuance time. | Proposal + Open question |
| G-08 | How the predecessor is obtained. | Closed | Step 2, obtaining the predecessor bullet: positional or by digest. | Proposal |
| G-09 | Chapter 01 step 5 vs chapter 03 Phase A on registrar confirmation. | Closed | Step 5 and chapter 03 Phase A, Phase E and reason code table: non-blocking by default, blocking indeterminate when `registrarConfirmationBlocking` is set. Offline registrar evidence format stays open question 13. | Proposal |
| G-10 | No anchoring profile. | Open | Open question 3. | Open question |
| G-11 | Confirmation depth default. | Partly closed | Step 6 now defers to chapter 03 Phase D (`minAnchorConfirmations`, `allowProvisionalAnchors`). The default value stays open (Q-009, chapter 03 open question 2). | Proposal + Open question |
| G-12 | Which fields may be omitted. | Closed | Field presence paragraph after the field table; `anchorReceipt` row. | Proposal |
| G-13 | Key encodings and types. | Closed | Key encodings: Multikey per W3C CID 1.0 section 2.2.2 (C-048), OKP JWK per RFC 8037 section 2 (C-049), exactly one, Ed25519 only in `0.1.0`. | Sourced formats + Proposal |
| G-14 | No suite registry; unsupported suite outcome. | Partly closed | Signature suites and step 3, unsupported suites bullet: not counted, warning if threshold met, else indeterminate `unsupported-suite`. Registry stays open question 11 (Q-034). | Proposal + Open question |
| G-15 | No code for a present but malformed field. | Closed | Step 1: `field-invalid`, added to chapter 03 reason codes. | Proposal |
| G-16 | `requiredSignatureCount` above signers; signers missing from keys. | Closed | `authorityPolicy` row: malformed, step 1 `field-invalid`. | Proposal |
| G-17 | `entityId` continuity unchecked. | Closed | `entityId` row and step 4: `entity-id-mismatch`, added to chapter 03. | Proposal |
| G-18 | "Return" in each step vs step 7 aggregation. | Closed | Evaluation order paragraph and step 7: steps record and continue (step 1 stops, step 2 indeterminate skips 3 and 4), aggregation as chapter 03 Phase E. | Proposal |
| G-19 | `delegationPolicy` shape and threshold interaction. | Partly closed | Delegation policy: array of delegation objects; delegate signatures not counted until open question 2 is resolved. | Proposal + Open question |
| G-20 | No list of supported versions. | Closed | `protocolVersion` row: this edition is `0.1.0`. | Proposal |
| G-21 | Who publishes official vectors. | Open | Verification method item 1 and open question 12 (Q-035). The vectors in `test-vectors/ch01/` remain reference vectors. | Open question |

Counting partly closed gaps once: closed 13 (G-02, G-03, G-04, G-05, G-08, G-09, G-12, G-13, G-15, G-16, G-17, G-18, G-20), partly closed 5 (G-06, G-07, G-11, G-14, G-19), open 3 (G-01, G-10, G-21).
