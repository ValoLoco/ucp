# Chapter 03: Verification

Status: discussion draft. Claim labels: [00-conventions.md](00-conventions.md). Cited facts: [docs/claims.md](../docs/claims.md). Builds on [01-entity-record.md](01-entity-record.md) (seven-step record verifier, field names, outcomes) and [02-entity-history.md](02-entity-history.md) (hash-linked history, fork detection, anchor semantics).

## Problem

Participants need a deterministic **history verifier** that consumes an entity history (chapter 01 records, chapter 02 hash links, and optional anchor receipts) and returns one of three outcomes: `valid`, `invalid`, or `indeterminate`, together with machine-readable **reason codes** suitable for automation and conformance tests.

**Verified fact (with source):** Chapter 01 normatively defines a seven-step verification sequence for a single entity record returning `valid`, `invalid`, or `indeterminate` with human-readable strings in a `reasons` array ([01-entity-record.md](01-entity-record.md)).

**Verified fact (with source):** Chapter 02 states that history-level evaluation MUST NOT introduce outcome labels beyond `valid`, `invalid`, or `indeterminate`, and that verifiers MUST apply chapter 01 steps 1 through 7 per record before history rules ([02-entity-history.md](02-entity-history.md)).

**Verified fact (with source):** Chapter 00 states that `effectiveAt` is a claimed time, not a trusted timestamp; verifiers MUST NOT treat it as proof of creation time. Trusted time comes from separate evidence such as anchor receipts under stated assumptions ([00-conventions.md](00-conventions.md)).

**Proposal:** This chapter normatively defines the history verifier algorithm, required inputs, inputs that MUST NOT be trusted, offline and light-lag behavior (stale revocation data, delayed anchor confirmations), a proposed reason code list, and conformance scenarios described in prose only. It does not select serialization, digest algorithm, or signature suite ([Q-005](../docs/claims.md)).

**Open question:** Whether a future chapter will define a canonical history bundle wire format; this verifier is defined over logical inputs (ordered records, hash links, optional anchor and revocation material) regardless of encoding ([Q-012](../docs/claims.md)).

## Existing alternatives

### OpenTimestamps verification

**Verified fact (with source):** OpenTimestamps states that a timestamp proves that some data existed prior to some point in time, and defines operations for creating provable timestamps that parties can verify later ([OpenTimestamps](https://opentimestamps.org/) (accessed 2026-11-24), [C-018](../docs/claims.md)).

**Verified fact (with source):** The OpenTimestamps client README documents that incomplete timestamps may require a remote calendar to supply a path to a Bitcoin block header, and that `ots upgrade` adds the path to the Bitcoin blockchain so the timestamp is complete ([OpenTimestamps client README](https://github.com/opentimestamps/opentimestamps-client/blob/master/README.md) (accessed 2026-11-24), [C-028](../docs/claims.md)).

**Proposal:** UCP anchor verification under an OpenTimestamps-named profile SHOULD accept upgraded proofs that verify from carried Bitcoin header data without live calendar access, subject to verifier policy ([Q-010](../docs/claims.md)).

### W3C Verifiable Credentials verification

**Verified fact (with source):** The VC Data Model defines machine-readable credentials and verification concepts ([W3C VC Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/) (accessed 2026-11-24), [C-008](../docs/claims.md)).

**Proposal:** Verification of embedded `legalRegistrations` credentials MAY follow VC verification patterns, but the entity history verifier MUST NOT treat credential validity as equivalent to legal recognition ([01-entity-record.md](01-entity-record.md)).

### Delay-tolerant networking and light lag

**Verified fact (with source):** Bundle Protocol version 7 is specified in [RFC 9171](https://www.rfc-editor.org/rfc/rfc9171.html) (accessed 2026-11-24), [C-021](../docs/claims.md)).

**Verified fact (with source):** NASA describes Earth-to-Mars command latency between 3 and 22 minutes for the Perseverance rover depending on orbital position ([NASA Science](https://science.nasa.gov/blog/speaking-percys-language-how-to-talk-so-perseverance-will-listen/) (accessed 2026-11-24), [C-019](../docs/claims.md)).

**Verified fact (with source):** A NASA communications disruption and delay white paper states that crewed Mars roundtrip missions face inevitable direct Earth link blackouts lasting weeks, with example blackout periods on the order of weeks in representative profiles ([NASA Mars communications disruption and delay PDF](https://www.nasa.gov/wp-content/uploads/2024/01/mars-communications-disruption-and-delay.pdf) (accessed 2026-11-24), [C-026](../docs/claims.md)).

**Verified fact (with source):** Blockstream Satellite documentation states that the network broadcasts the Bitcoin blockchain worldwide around the clock, including blocks and complete block history for synchronization ([Blockstream Satellite](https://blockstream.github.io/satellite/) (accessed 2026-11-24), [C-025](../docs/claims.md)).

**Proposal:** The history verifier MUST operate on carried proof data plus verifier-supplied Bitcoin chain data under stated policy, without requiring live calls to proprietary registrar APIs or OpenTimestamps calendars once proofs are complete per profile assumptions.

## Proposal

### Scope and explicit non-goals

This chapter normatively defines:

- A **history verifier** that takes an ordered entity history and returns `status`, `reasonCodes`, and optionally `reasons` and `warnings` as specified below.
- Required inputs and inputs a verifier MUST NOT trust.
- Offline and light-lag verification behavior including stale revocation data and delayed anchor confirmations.
- A proposed list of machine-readable reason codes.
- Conformance test vectors described in prose only (no wire format).

This chapter explicitly does **not** specify:

- A wire format for history bundles ([02-entity-history.md](02-entity-history.md) does not normatively profile transport).
- Canonical serialization, digest algorithm, or signature suite ([Q-005](../docs/claims.md)).
- Legal recognition of any verification outcome.
- A revocation registry protocol (unsettled in chapter 01).
- Fork resolution tie-breakers ([Q-006](../docs/claims.md); chapter 02 preserves `indeterminate` with `competing successors` until policy exists).

### Result object (normative)

A conforming history verifier MUST return an object with:

| Field | Required | Description |
| --- | --- | --- |
| `status` | yes | One of `valid`, `invalid`, or `indeterminate` only. |
| `reasonCodes` | yes | Array of machine-readable strings (may be empty when `status` is `valid` and no warnings apply). |
| `reasons` | SHOULD | Array of human-readable strings aligned with chapter 01 style where applicable. |
| `warnings` | SHOULD when non-empty | Array of reason codes (or short strings) for non-blocking conditions that did not change `status` from `valid` to `indeterminate` under verifier policy. |

History-level evaluation MUST NOT introduce status values other than the three named in chapter 01 and chapter 02.

### Required verifier inputs

A conforming verifier MUST accept at minimum:

1. **Record set:** One or more entity records conforming to chapter 01 sharing a single `entityId` under test, including an ordered **tip chain** from genesis to the record under review (see Input validation below).
2. **Hash links:** For each non-genesis record in the tip chain, chapter 02 append-only rules apply; the verifier MUST be able to compute or obtain each predecessor digest under the active signing profile ([Q-005](../docs/claims.md)).
3. **Anchor material** (optional): For records with `anchorReceipt`, data needed to verify the external commitment under the named anchoring profile (for example upgraded OpenTimestamps proof bytes and referenced Bitcoin headers).
4. **Revocation material** (optional): Carried lists or status objects referenced by `revocationRef` in `authorizedKeys` or delegations.
5. **Bitcoin chain data** (optional): Headers or condensed chain data sufficient to check confirmation depth under policy when anchor verification requires it.
6. **Verification policy:** A local policy object specifying at least:
   - Supported `protocolVersion` values.
   - Accepted anchoring profiles and confirmation depth assumptions ([Q-009](../docs/claims.md)).
   - Whether external registrar confirmation is required for `legalRegistrations` (if required and unavailable, see chapter 01 step 5).
   - `maxRevocationDataAge` for offline verification (see below).
   - `minAnchorConfirmations` and `allowProvisionalAnchors` for light-lag and offline anchor behavior.

### Inputs a verifier MUST NOT trust

Without independent verification under chapter 01 and chapter 02 rules, a verifier MUST NOT treat as authoritative:

- `effectiveAt` in any record ([00-conventions.md](00-conventions.md)).
- `previousRecordDigest` without matching the digest computed for the obtained predecessor (chapter 01 step 4; chapter 02 conflicting-record rules).
- `anchorReceipt` presence without profile verification and stated confirmation assumptions.
- `legalRegistrations` or embedded credentials as proof of legal recognition.
- Revocation status from data older than `maxRevocationDataAge` in policy (stale revocation data).
- Anchor confirmation from chain data that does not meet `minAnchorConfirmations` unless `allowProvisionalAnchors` waives blocking behavior.
- Any record field not bound by the signature payload once serialization is standardized ([Q-005](../docs/claims.md)).

### History verifier algorithm (normative)

A conforming verifier MUST implement the following phases. Record-level cryptography and fields MUST use the chapter 01 seven-step sequence without contradicting it. Fork and multi-record graph rules MUST follow chapter 02 **Fork and conflicting-record detection** without redefining fork semantics.

#### Phase A: Input validation

If the supplied tip chain is empty, return `invalid` with `reasonCodes` containing `empty-chain`.

If the genesis record in the tip chain has non-null `previousRecordDigest`, return `invalid` with `reasonCodes` containing `genesis-previous-not-null`.

If more than one record in the bundle has `previousRecordDigest: null` for the same `entityId` and policy does not define allowed regenesis, return `indeterminate` with `reasonCodes` containing `ambiguous-genesis` (chapter 02 verification method item 2).

For each record in the tip chain, run the chapter 01 seven-step sequence with these history-specific inputs:

- **Step 2:** The predecessor MUST be the prior record in the supplied tip chain when contiguous; if the chain skips an intermediate digest, return `indeterminate` with `chain-gap` and reason `chain gap` in `reasons`.
- **Step 5:** If policy requires external registrar confirmation that is unavailable, record a non-blocking `registrar-confirmation-unavailable` code on the record result (chapter 01 step 5).
- **Step 6:** Apply anchor rules in Phase D; if required Bitcoin data is missing and policy does not allow provisional anchors, record blocking `anchor-data-unavailable`.

Collect per-record `status` and reason information.

#### Phase B: Chain integrity and forks

For each non-genesis record in the tip chain, verify digest linkage per chapter 02 item 4: if `previousRecordDigest` does not match the computed predecessor digest, return `invalid` with `digest-mismatch` at that position.

Apply chapter 02 fork detection (collect records, build predecessor graph, detect competing successors). If more than one successor attaches to the same predecessor digest and policy does not select a winner, return `indeterminate` with `competing-successors` and human reason `competing successors` ([Q-006](../docs/claims.md)).

#### Phase C: Key continuity and revocation

For each transition from record *i-1* to record *i* in the tip chain:

- Confirm `authorizedKeys` changes are authorized per `authorityPolicy` on record *i-1* (signatures on record *i* satisfy required count).
- For each signing key on record *i*, evaluate revocation using carried revocation material and `maxRevocationDataAge`.
- If a key is revoked per fresh material, return `invalid` with `key-revoked`.
- If material is older than `maxRevocationDataAge`, treat as `revocation-data-stale` (non-blocking warning when other checks pass).
- If `revocationRef` is present and no material is supplied, return `indeterminate` with `revocation-data-missing`.

#### Phase D: Anchor verification (per record)

For each record carrying `anchorReceipt`:

- Verify the proof under the named profile. Cryptographic failure yields `invalid` with `anchor-proof-invalid`.
- If the anchor commits to a digest that does not match the record digest under policy, return `invalid` with `anchor-digest-mismatch`.
- If confirmation depth is required and supplied chain data shows fewer than `minAnchorConfirmations`, apply `anchor-confirmations-insufficient` (blocking `indeterminate` unless `allowProvisionalAnchors` moves it to `warnings`).
- If confirmation depth is required and no chain data is supplied, apply `anchor-data-unavailable` (blocking unless provisional policy applies as in Phase E).

When an OpenTimestamps-style profile is used, incomplete proofs that still require live calendar assistance MUST NOT yield `valid` anchor step results until upgraded or cached per client documentation ([C-028](../docs/claims.md), [Q-010](../docs/claims.md)).

#### Phase E: Aggregation

Aggregate per-record and history-level results:

1. If any phase yields `invalid`, chain `status` is `invalid`. `reasonCodes` MUST be the union of all invalid codes (deduplicated).
2. Else if any blocking `indeterminate` condition is present (`chain-gap`, `competing-successors`, `predecessor-unavailable`, `policy-unresolvable`, `revocation-data-missing`, `anchor-data-unavailable` when not waived, or blocking `anchor-confirmations-insufficient`), chain `status` is `indeterminate` with the union of blocking codes in `reasonCodes`.
3. Else if only non-blocking conditions remain (`registrar-confirmation-unavailable`, `revocation-data-stale`, provisional anchor codes), chain `status` is `valid` and those codes appear in `warnings`.
4. Else chain `status` is `valid` with empty `reasonCodes` and empty `warnings`.

**Note:** This preserves chapter 01 intent that `indeterminate` is returned when evidence is incomplete ([01-entity-record.md](01-entity-record.md) step 7 note), including partitioned networks and unresolved forks.

### Offline and light-lag verification

**Assumption:** Verifiers in disconnected or high-latency environments ([C-019](../docs/claims.md), [C-026](../docs/claims.md)) operate on bundles received via store-and-forward transport ([C-021](../docs/claims.md)) and MAY receive Bitcoin blocks asynchronously ([C-025](../docs/claims.md)).

**Proposal:** Verifier policy MUST document:

- `maxRevocationDataAge`: maximum age of carried revocation material. Older material MUST yield `revocation-data-stale` (warning when policy treats staleness as non-blocking).
- `minAnchorConfirmations`: minimum confirmations for non-provisional `valid` anchor results ([Q-009](../docs/claims.md)).
- `allowProvisionalAnchors`: when true, `anchor-confirmations-insufficient` and `anchor-data-unavailable` MAY downgrade to `warnings` if the anchor proof structure is otherwise cryptographically valid under profile rules.

**Proposal:** When Bitcoin chain data is entirely unavailable, anchored records MUST NOT contribute blocking `indeterminate` solely for missing confirmations if `allowProvisionalAnchors` is true and the proof verifies structurally; the verifier MUST emit `anchor-confirmations-unverified` in `warnings`.

### Proposed reason codes (machine-readable)

The following reason codes are **proposal** until implementer experience confirms stability ([Q-012](../docs/claims.md)). Codes use lowercase ASCII with hyphen separators. Each code SHOULD appear at most once per verification result unless the implementation documents indexed instances (for example digest position).

| Code | Typical `status` | Maps to chapter 01 human reason (if any) |
| --- | --- | --- |
| `empty-chain` | invalid | (history-level) |
| `genesis-previous-not-null` | invalid | (history-level) |
| `ambiguous-genesis` | indeterminate | (history-level) |
| `missing-field` | invalid | step 1 |
| `unsupported-protocol-version` | invalid or indeterminate | step 1 |
| `predecessor-unavailable` | indeterminate | `predecessor unavailable` (step 2) |
| `chain-gap` | indeterminate | `chain gap` |
| `policy-unresolvable` | indeterminate | step 2 |
| `signature-missing` | invalid | step 3 |
| `signature-invalid` | invalid | step 3 |
| `key-expired` | invalid | step 3 |
| `key-revoked` | invalid | step 3 |
| `revocation-data-stale` | warning | step 3 |
| `revocation-data-missing` | indeterminate | step 3 |
| `digest-mismatch` | invalid | step 4 |
| `competing-successors` | indeterminate | `competing successors` (step 4; chapter 02) |
| `registrar-confirmation-unavailable` | warning | step 5 |
| `anchor-proof-invalid` | invalid | step 6 |
| `anchor-digest-mismatch` | invalid | step 6 |
| `anchor-confirmations-insufficient` | indeterminate or warning | step 6 |
| `anchor-data-unavailable` | indeterminate or warning | step 6 |
| `anchor-confirmations-unverified` | warning | step 6 |

### Conformance test vectors (prose only)

Implementations MUST satisfy the following scenarios. Inputs are described logically; no serialization is specified.

1. **Valid genesis, no anchor:** Single-record tip chain, genesis with `previousRecordDigest: null`, valid signatures, no `anchorReceipt`. Policy: no registrar confirmation required. Expected: `status: valid`, empty `reasonCodes`, empty `warnings`.

2. **Valid two-record chain with anchor:** Genesis plus one successor with matching `previousRecordDigest`, valid signatures, upgraded anchor with six confirmations in supplied chain data. Policy: `minAnchorConfirmations: 6`, `allowProvisionalAnchors: false`. Expected: `valid`.

3. **Anchor confirmations insufficient, blocking:** As test 2 but chain data shows three confirmations. Expected: `indeterminate`, `reasonCodes` includes `anchor-confirmations-insufficient`.

4. **Anchor confirmations insufficient, provisional:** As test 3 with `allowProvisionalAnchors: true`. Expected: `valid`, `warnings` includes `anchor-confirmations-insufficient`.

5. **Offline anchor, provisional allowed:** As test 2 without Bitcoin chain data; `allowProvisionalAnchors: true`. Expected: `valid`, `warnings` includes `anchor-confirmations-unverified`.

6. **Offline anchor, provisional disallowed:** As test 5 with `allowProvisionalAnchors: false`. Expected: `indeterminate`, `reasonCodes` includes `anchor-data-unavailable`.

7. **Competing successors:** Genesis plus two distinct successors with the same valid `previousRecordDigest`. Expected: `indeterminate`, `reasonCodes` includes `competing-successors` (chapter 02 fork rules).

8. **Chain gap:** Genesis plus successor whose predecessor digest does not match genesis (missing intermediate record). Expected: `indeterminate`, `reasonCodes` includes `chain-gap`.

9. **Key revoked within policy age:** Successor signed with key listed as revoked in carried material within `maxRevocationDataAge`. Expected: `invalid`, `reasonCodes` includes `key-revoked`.

10. **Revocation data stale:** Carried revocation timestamp older than `maxRevocationDataAge`. Expected: `valid`, `warnings` includes `revocation-data-stale`.

11. **Revocation data missing:** Key has `revocationRef`, no material supplied. Expected: `indeterminate`, `reasonCodes` includes `revocation-data-missing`.

12. **Digest mismatch:** Successor `previousRecordDigest` does not match computed genesis digest. Expected: `invalid`, `reasonCodes` includes `digest-mismatch`.

13. **Registrar confirmation required, offline:** Policy requires registrar confirmation; records otherwise valid. Expected: `valid`, `warnings` includes `registrar-confirmation-unavailable`.

14. **Anchor proof invalid:** Present `anchorReceipt` but profile verification fails. Expected: `invalid`, `reasonCodes` includes `anchor-proof-invalid`.

15. **Anchor digest mismatch:** Anchor commits to digest D1, record digest is D2. Expected: `invalid`, `reasonCodes` includes `anchor-digest-mismatch`.

16. **Light-lag bundle:** Tip chain and anchor proofs arrive via delay-tolerant bundle ([C-021](../docs/claims.md)). Mars-side verifier has chain data only through height H while Earth proved height H+6. Policy: `minAnchorConfirmations: 6`, `allowProvisionalAnchors: true`, `maxRevocationDataAge: 60 days`. Expected: `valid` with `warnings` for anchors that cannot locally confirm required depth ([C-019](../docs/claims.md), [C-026](../docs/claims.md)).

### Mapping from chapter 01 steps

| Chapter 01 step | Chapter 03 usage |
| --- | --- |
| 1. Format and protocol version | Phase A per record |
| 2. Predecessor and policy | Phase A; predecessor from tip chain |
| 3. Signatures and keys | Phase A and Phase C |
| 4. Sequence and conflicts | Phase B; fork detection references chapter 02 |
| 5. Registration evidence | Phase A non-blocking registrar code |
| 6. Anchor receipt | Phase A and Phase D |
| 7. Report | Phase E aggregation with `reasonCodes` |

## Trust assumptions

- Verifiers implement chosen cryptographic suites correctly once standardized ([01-entity-record.md](01-entity-record.md)).
- Predecessor records, revocation material, and Bitcoin headers needed by policy are included in the bundle or the verifier reports `indeterminate` honestly.
- Bitcoin proof-of-work chain selection and confirmation depth follow stated policy ([02-entity-history.md](02-entity-history.md)).
- OpenTimestamps calendar servers are not long-term verification dependencies after proofs are complete ([C-028](../docs/claims.md)).
- `valid` verification is not legal recognition, registrar confirmation, or securities compliance.
- Carried revocation material reflects issuer belief at its stated time; staleness handling is policy, not cryptographic truth.

## Legal implications

This chapter does **not** claim that a `valid` verification result creates legal persons, binds third parties, satisfies KYC or AML rules, or replaces statutory registers.

**Verified fact (with source):** States bear responsibility under the Outer Space Treaty for authorizing and supervising non-governmental space activities ([C-002](../docs/claims.md)). Portable verification outcomes do not remove that obligation.

**Open question:** Whether UNCITRAL Model Law on Identity Management and Trust Services (2022) defines trust-service concepts that should align with `authorityPolicy` or verifier policy ([Q-008](../docs/claims.md)).

Unsettled items belong in Open questions and qualified legal review.

## Privacy impact

- Verification MAY run entirely on carried bundles without live registrar or calendar queries, reducing query metadata leakage.
- History verification reveals update cadence, keys, and registration claims; operators SHOULD minimize published fields ([02-entity-history.md](02-entity-history.md)).
- Calendar stamping discloses digests to calendars ([C-018](../docs/claims.md)); verification after upgrade does not require re-disclosure.
- Carried revocation lists may reveal compromise events; bundlers SHOULD minimize included material.
- Provisional anchor acceptance trades finality for availability; relying parties SHOULD understand probabilistic evidence.

## Verification method

Independent conformance review MUST:

1. Implement Phases A through E.
2. Execute prose test vectors 1 through 16.
3. Confirm `reasonCodes` match expected codes per scenario.
4. Confirm `indeterminate` when predecessors, revocation material, or anchor chain data are withheld unless policy waives blocking behavior.
5. Confirm chapter 01 seven-step behavior is invoked per record without contradiction.
6. Confirm examples use fictional **Example Jurisdiction** values only.
7. Run offline tests with no network except carried data.
8. Simulate light-lag by supplying stale Bitcoin height relative to proof claims.

## Smallest useful test

Apply the chapter 00 pull request checklist from [00-conventions.md](00-conventions.md#smallest-useful-test) to this file.

Minimal falsification experiments:

1. Two-record tip chain with mismatched `previousRecordDigest`: expect `invalid` and `digest-mismatch`.
2. Two competing successors of one genesis in the bundle: expect `indeterminate` and `competing-successors`.
3. Valid OpenTimestamps structure with three confirmations and `minAnchorConfirmations: 6`, `allowProvisionalAnchors: false`: expect `indeterminate` and `anchor-confirmations-insufficient`.
4. Same as 3 with `allowProvisionalAnchors: true`: expect `valid` with warning `anchor-confirmations-insufficient`.
5. Revoked key within `maxRevocationDataAge`: expect `invalid` and `key-revoked`.
6. `revocationRef` without carried data: expect `indeterminate` and `revocation-data-missing`.
7. Offline verification with upgraded proof and `allowProvisionalAnchors: true`: expect `valid` with `anchor-confirmations-unverified`.

## Open questions

1. **Verification (external experts):** Should the reason code list in this chapter become normative in the next protocol minor version, or remain proposal until two independent implementations pass all sixteen prose vectors ([Q-012](../docs/claims.md))?

2. **Verification (external experts):** What default values for `maxRevocationDataAge` and `minAnchorConfirmations` should pilots publish for high-consequence updates versus routine updates?

3. **Verification (external experts):** MUST conforming implementations emit chapter 01 `reasons` strings whenever they emit `reasonCodes`, and is a published mapping table required for interoperability ([Q-013](../docs/claims.md))?

4. **Verification (external experts):** Should the `warnings` array be normative for non-blocking conditions, or should warnings appear only in informative logs outside the result object ([Q-014](../docs/claims.md))?

5. **Bitcoin timestamping:** Which Bitcoin light-client verification approach (full node, assumeUTXO, compact filters) should conformance tests recommend for offline confirmation checks ([Q-015](../docs/claims.md))?

6. **Bitcoin timestamping:** How MUST verifiers treat reorganizations below `minAnchorConfirmations` when `allowProvisionalAnchors` is true ([Q-009](../docs/claims.md))?

7. **Space operations (external experts):** During Mars conjunction-style blackout windows ([C-026](../docs/claims.md)), should verifier policy temporarily raise `maxRevocationDataAge` or default `allowProvisionalAnchors` to true, and how should operators authenticate blackout schedules without trusted network time?

8. **Space operations:** Should history bundles normatively declare the Bitcoin block height horizon available at bundle creation so distant verifiers can explain `anchor-confirmations-unverified` warnings ([Q-016](../docs/claims.md))?

9. **Identity (external experts):** Which combination of LEI, vLEI credentials ([C-013](../docs/claims.md)), and portable `entityId` strings should history verifiers require in policy for cross-border pilots?

10. **Law (external experts):** Does UNCITRAL MLIT (2022) offer trust-service categories that map to verifier policy fields ([Q-008](../docs/claims.md))?

11. **Governance:** Should verifier policy objects themselves be signed entity records in the history chain, or remain out-of-band configuration ([Q-017](../docs/claims.md))?

12. **Transport:** When a canonical history bundle format is defined, must reason codes be stable across bundle encodings ([Q-012](../docs/claims.md))?