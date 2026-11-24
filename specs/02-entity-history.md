# Chapter 02: History and timestamping

Status: discussion draft. Claim labels: [00-conventions.md](00-conventions.md). Cited facts: [docs/claims.md](../docs/claims.md). Builds on [01-entity-record.md](01-entity-record.md) for record fields, digests, and verifier outcomes `valid`, `invalid`, and `indeterminate`.

## Problem

A portable entity record that must be examined across jurisdictions, offline periods, and long one-way light delays needs more than isolated signed snapshots. Participants need an append-only, hash-linked history so independent verifiers can confirm update order, detect forks and conflicting successors, and obtain optional "existed before" evidence that does not depend on a trusted timestamp authority or a live proprietary API.

**Proposal:** Chapter 02 normatively specifies how multiple [01-entity-record.md](01-entity-record.md) versions form one logical history for an `entityId`, how fork and conflict conditions are detected and reported, and how optional `anchorReceipt` values relate to trusted time without contradicting chapter 01 rules for `effectiveAt`, field names, and the seven-step verifier.

## Existing alternatives

### OpenTimestamps

**Verified fact (with source):** OpenTimestamps states that a timestamp proves that some data existed prior to some point in time ([OpenTimestamps](https://opentimestamps.org/) (accessed 2026-11-24), [C-018](../docs/claims.md)).

**Verified fact (with source):** The `opentimestamps-client` package version 0.8.0 was published on 2026-10-27 ([PyPI](https://pypi.org/project/opentimestamps-client/) (accessed 2026-11-24), [C-020](../docs/claims.md)).

**Verified fact (with source):** The OpenTimestamps site documents free-to-use calendar servers that perform stamping on behalf of users and do not require registration ([OpenTimestamps](https://opentimestamps.org/) (accessed 2026-11-24), [C-027](../docs/claims.md)).

**Proposal:** OpenTimestamps supplies Bitcoin-linked existence-before evidence for a digest. It does not, by itself, define an entity-specific hash-linked update chain, `authorityPolicy`, fork resolution, or UCP verifier semantics. UCP MAY carry OpenTimestamps-style metadata inside `anchorReceipt` once a profile is chosen ([Q-009](../docs/claims.md)).

### Nostr NIP-03

**Verified fact (with source):** Nostr NIP-03 defines kind `1040` events that carry a base64-encoded `.ots` proof for another event and is marked **unrecommended** with text stating it is vulnerable to one specific attack and needs update ([NIP-03](https://nips.nostr.com/3) (accessed 2026-11-24), [C-024](../docs/claims.md)).

**Proposal:** UCP history transport MUST NOT depend on NIP-03 relays. Entities MAY still reuse OpenTimestamps proofs independent of Nostr.

### DID methods anchored to Bitcoin

**Verified fact (with source):** The `did:btcr2` method specification states it is under active development and may be subject to breaking changes ([did:btcr2](https://dcdpr.github.io/did-btcr2/) (accessed 2026-11-24), [C-015](../docs/claims.md)).

**Verified fact (with source):** The `decentralized-identity/ion` repository last received a default-branch push on 2023-08-25 ([GitHub ion](https://github.com/decentralized-identity/ion) (accessed 2026-11-24), [C-016](../docs/claims.md)).

**Proposal:** Bitcoin-anchored DID operation logs address identifier documents, not the full UCP entity record object model in [01-entity-record.md](01-entity-record.md). UCP history verification MUST remain verifiable from carried records and optional anchor data without assuming a particular DID resolver stays online.

### Bitcoin blockchain broadcast (offline confirmation)

**Verified fact (with source):** Blockstream Satellite documentation states that the network broadcasts the Bitcoin blockchain worldwide 24/7 for free, including new blocks, transactions, and complete block history for synchronization ([Blockstream Satellite](https://blockstream.github.io/satellite/) (accessed 2026-11-24), [C-025](../docs/claims.md)).

**Assumption:** One-way reception of Bitcoin blocks MAY help verifiers confirm anchor receipts when interactive Internet access is intermittent. It does not prove entity legality, signer authority, or record uniqueness at anchoring time.

### Store-and-forward networking

**Verified fact (with source):** Bundle Protocol version 7 is specified in [RFC 9171](https://www.rfc-editor.org/rfc/rfc9171.html) (accessed 2026-11-24), [C-021](../docs/claims.md)).

**Proposal:** Histories, predecessor bundles, revocation material, and optional anchor receipts MAY be carried in delay-tolerant bundles. This chapter does not normatively profile BPv7 endpoints, convergence layers, or custody semantics.

### Light lag and Mars communications disruption

**Verified fact (with source):** NASA describes Earth-to-Mars command latency between 3 and 22 minutes for the Perseverance rover depending on orbital position ([NASA Science](https://science.nasa.gov/blog/speaking-percys-language-how-to-talk-so-perseverance-will-listen/) (accessed 2026-11-24), [C-019](../docs/claims.md)).

**Verified fact (with source):** A NASA Moon to Mars architecture white paper on communications disruption and delay states that for any crewed roundtrip mission to Mars, direct spacecraft-to-Earth communications blackouts are inevitable and can last weeks, and gives example analyses with blackout periods on the order of weeks or about 13 to 21 days for representative mission profiles ([NASA Mars communications disruption and delay PDF](https://www.nasa.gov/wp-content/uploads/2024/01/mars-communications-disruption-and-delay.pdf) (accessed 2026-11-24), [C-026](../docs/claims.md)).

**Proposal:** Commercial low-Earth-orbit relay constellations extended to Mars for general commerce remain design proposals in this repository ([P-001](../docs/claims.md)), not operational prerequisites for UCP history verification.

## Proposal

### Relationship to chapter 01

This chapter does not redefine entity record fields. Each history element is one entity record as defined in [01-entity-record.md](01-entity-record.md). Verifiers MUST apply the seven-step sequence from chapter 01 to each record under test, then apply the history rules below when more than one record shares an `entityId`.

Outcomes remain exactly `valid`, `invalid`, or `indeterminate` with a `reasons` array. History-level evaluation MUST NOT introduce additional outcome labels.

### Append-only hash-linked history (normative)

An **entity history** is a directed sequence of entity records that share the same `entityId` and form a hash-linked chain using `previousRecordDigest` as named in chapter 01.

- The **genesis record** for an `entityId` MUST set `previousRecordDigest` to `null`.
- Every subsequent record MUST set `previousRecordDigest` to the digest of exactly one prior record that the issuer claims as its sole immediate predecessor.
- Issuers MUST NOT publish a new accepted record that replaces or deletes a prior digest commitment. Corrections MUST appear only as later records that cite the prior digest and state the change under `authorityPolicy` rules.

The digest algorithm and canonical signing input remain unset ([Q-005](../docs/claims.md)). Until selected, history links are defined logically: the digest of record *n* is the value that record *n+1* places in `previousRecordDigest`.

Verifiers MUST obtain the predecessor record (or its digest under the active profile) to validate step 4 in chapter 01. If the predecessor is missing from the bundle, verifiers MUST return `indeterminate` with reason consistent with chapter 01 (`predecessor unavailable`).

### Fork and conflicting-record detection (normative)

A **fork** exists when two or more records share the same `entityId`, the same resolved `previousRecordDigest`, valid signatures under the authority state applicable at that point, and pairwise-distinct record digests or materially distinct signed content.

A **conflicting record** is any record that fails digest linkage (claimed predecessor digest does not match the obtained predecessor) or violates `authorityPolicy` for the claimed update.

Verifiers MUST:

1. Collect all records in the bundle with the same `entityId`.
2. Build a predecessor graph keyed by digest.
3. If more than one successor attaches to the same predecessor digest and local policy does not select a unique winner, return `indeterminate` with reason `competing successors` ([Q-006](../docs/claims.md)), matching chapter 01 step 4.
4. If `previousRecordDigest` does not match the digest computed for the obtained predecessor, return `invalid` with an explicit digest mismatch reason.
5. When reporting history-level results, include the set of fork tips (records with no known successor in the bundle) when multiple tips exist.

**Proposal:** Future chapters MAY define tie-breakers using earliest valid anchor receipt under Bitcoin ordering assumptions, lexicographic digest order, or human-governed multi-signature recovery. Until adopted, absence of a tie-breaker preserves `indeterminate`.

### Optional Bitcoin anchor receipts (normative behavior, open profile)

The `anchorReceipt` field MAY be present on any record version per chapter 01. When present, it SHOULD use an OpenTimestamps-style proof or another named profile that commits the record digest (or a Merkle root that commits the record digest) to Bitcoin block headers.

Under stated verifier assumptions (longest proof-of-work chain, sufficient confirmation depth ([Q-009](../docs/claims.md)), and successful cryptographic verification of the proof), an anchor receipt provides **existence-before** evidence: the committed digest was known to the issuer before the referenced Bitcoin block time encoded in the proof.

**Assumption:** Bitcoin block timestamps are median-time hints subject to protocol rules ([C-007](../docs/claims.md)); verifiers SHOULD document confirmation depth and clock interpretation in verifier policy.

#### What anchoring does and does not prove

| Anchoring establishes (under assumptions) | Anchoring does **not** establish |
| --- | --- |
| The committed digest existed before the anchored block time under stated Bitcoin confirmation rules | Legal truth of record fields, corporate status, or registrar acceptance |
| An independent party can re-verify the proof given chain headers | That signers had legal authority or that signatures bind a contract in any jurisdiction |
| A global ordering hint for when the digest entered a public commitment | Absence of a competing fork of the entity history at anchor time |
| | That `effectiveAt` is accurate |

**Verified fact (with source):** Repository research notes state that anchoring is a commitment under stated verification assumptions, not absolute finality or proof of legal truth ([docs/research/assumptions-and-corrections.md](../docs/research/assumptions-and-corrections.md)).

Verifiers MUST NOT treat a verified anchor receipt as substituting for steps 2 through 5 in chapter 01. Failure of anchoring step 6 yields `invalid` for cryptographic failure or `indeterminate` when required chain data is temporarily unavailable, per chapter 01.

### Trusted time versus `effectiveAt`

`effectiveAt` remains a claimed effective time only ([00-conventions.md](00-conventions.md)). Verifiers MUST NOT treat `effectiveAt` as proof of creation, notarization, or filing time.

When both `effectiveAt` and a verified `anchorReceipt` are present, verifiers SHOULD report them separately in `reasons` and MUST NOT merge them into a single trusted timestamp without explicit verifier policy.

### Offline and light-lag verification

**Proposal:** A conforming deployment SHOULD support **store-and-forward** distribution:

- Bundle complete history segments, predecessor records, revocation references, and optional upgraded OpenTimestamps proofs.
- Accept that verification may return `indeterminate` until predecessors or Bitcoin headers arrive ([01-entity-record.md](01-entity-record.md)).
- Prefer anchor proof upgrade paths that remove dependence on calendar servers remaining online ([Q-010](../docs/claims.md)).

Under long one-way delays ([C-001](../docs/claims.md), [C-019](../docs/claims.md)) or multi-week Earth-Mars communications blackout windows described for crewed mission analyses ([C-026](../docs/claims.md)), operators SHOULD plan for autonomous issuance and verification with cached keys, local bundles, and optional satellite-received Bitcoin blocks ([C-025](../docs/claims.md)).

### Privacy and public anchors

**Proposal:** Only the record digest, or a Merkle root that includes the digest, SHOULD be committed in public anchor structures. Full records, personal identity documents, confidential contracts, inline credentials, and private `documents` URIs MUST stay off public anchors unless the entity explicitly accepts the privacy risk.

OpenTimestamps calendar servers learn digests presented for stamping ([C-018](../docs/claims.md)). Operators SHOULD treat calendar submission as a disclosure event.

## Trust assumptions

- Participants agree on digest and signature profiles once standardized ([Q-005](../docs/claims.md)).
- Predecessor records and revocation material are available or verifiers honestly return `indeterminate`.
- Bitcoin anchoring assumes honest-majority proof-of-work chain selection and verifier-chosen confirmation depth (**assumption**).
- Calendar servers used at stamp time are not trusted for long-term verification once proofs are upgraded (**assumption**, [C-027](../docs/claims.md)).
- Fork resolution rules beyond `competing successors` remain unset ([Q-006](../docs/claims.md)).

## Legal implications

This chapter does not claim that hash-linked histories create legal persons, binding corporate acts, securities compliance, or recognition by registrars or courts.

**Verified fact (with source):** The Outer Space Treaty Article VI requires state authorization and supervision of non-governmental space activities ([C-002](../docs/claims.md)). A portable history does not satisfy national licensing by itself (**assumption**).

**Verified fact (with source):** [STATUS.md](../STATUS.md) states that no participating jurisdictions, endorsements, or legal recognition are claimed for UCP.

Whether Bitcoin-anchored existence-before evidence affects dispute resolution, notarization comparators, or supervised space operations is an open question for qualified counsel and domain experts (see Open questions). No legal effect in this chapter is labeled verified fact.

## Privacy impact

- Public anchors SHOULD carry digests only; rich metadata in records remains off-chain by default.
- History traversal reveals update frequency, key rotation, and registration claims; operators SHOULD minimize fields published in widely replicated bundles.
- Forks reveal dispute or partition events; parties SHOULD anticipate that competing successors become visible to anyone holding the bundle.

## Verification method

History conformance review MUST:

1. Apply chapter 01 steps 1 through 7 per record.
2. Verify genesis uniqueness per `entityId` in the bundle (at most one record with `previousRecordDigest: null` unless policy allows explicit regenesis, which this chapter does not define).
3. Walk `previousRecordDigest` links and apply fork rules in this chapter.
4. When `anchorReceipt` is present, verify under a documented profile and report anchoring separately from `effectiveAt`.
5. Confirm outcomes use only `valid`, `invalid`, or `indeterminate`.

## Smallest useful test

1. Publish a three-record fictional chain where record 2 and record 3 link via `previousRecordDigest`, upgrade an OpenTimestamps proof for record 3, and demonstrate chapter 01 step 6 returns `valid` under a stated confirmation assumption.
2. Publish `record-2-prime` sharing the same predecessor as record 2 with different signed content and demonstrate history evaluation returns `indeterminate` with `competing successors`.
3. Mutate a signed field after signing and demonstrate step 3 returns `invalid`.
4. Omit the predecessor from the bundle and demonstrate step 2 returns `indeterminate`.
5. Present a record whose signature uses a key already revoked in `authorizedKeys` and demonstrate step 3 returns `invalid` with an explicit revocation reason.

### Example (fictional, not a wire format)

The following illustrates a three-record history for **Example Jurisdiction** only. Digest strings, keys, and proofs are fictional.

**Record 1 (genesis):**

```json
{
  "protocolVersion": "0.1.0",
  "entityId": "ucp:entity:fictional-example-portable-collective",
  "legalRegistrations": [
    {
      "jurisdiction": "Example Jurisdiction",
      "officialId": "EJ-0000-0000",
      "evidence": ["ipfs://bafy-fictional-genesis-evidence"]
    }
  ],
  "authorizedKeys": [
    {
      "id": "key-fict-01",
      "publicKeyMultibase": "z6Mk-fictional-key-01",
      "role": "administrator",
      "validFrom": "2026-01-01T00:00:00Z"
    }
  ],
  "authorityPolicy": {
    "authorizedSigners": ["key-fict-01"],
    "requiredSignatureCount": 1
  },
  "documents": [],
  "previousRecordDigest": null,
  "effectiveAt": "2026-01-15T10:00:00Z",
  "signatures": [
    {
      "keyId": "key-fict-01",
      "suite": "fictional-suite-pending-selection",
      "signature": "fictional-sig-1"
    }
  ],
  "anchorReceipt": null
}
```

**Record 2 (adds governing document digest):** same entity and keys; `previousRecordDigest` is `sha256:fictional-digest-of-record-1`; adds a `documents` entry; `effectiveAt` is `2026-02-01T12:00:00Z`; signed by `key-fict-01`.

**Record 3 (key rotation with anchor receipt):** adds `key-fict-02`, sets `revocationRef` on `key-fict-01` with effect before signing time, updates `authorityPolicy.authorizedSigners` to `["key-fict-02"]`, links `previousRecordDigest` to record 2, and includes a fictional OpenTimestamps-style `anchorReceipt` committing to the record 3 digest. Record 3 MUST be signed by `key-fict-02` only. A variant that signs with `key-fict-01` after revocation illustrates an **invalid** history step for test vector 5.

**Invalid fork illustration:** `record-2-prime` copies record 2's `previousRecordDigest` but changes a `documents` digest. Verifiers report `competing successors` when both record 2 and `record-2-prime` are in the bundle.

## Open questions

1. **Bitcoin timestamping:** What confirmation depth and reorganisation policy MUST verifiers apply before an `anchorReceipt` can support `valid` for high-value updates ([Q-009](../docs/claims.md))?
2. **Bitcoin timestamping:** MUST operators require OpenTimestamps proof upgrade before treating calendar-dependent proofs as offline-verifiable ([Q-010](../docs/claims.md))?
3. **Bitcoin timestamping:** Should UCP standardize a single `anchorReceipt` profile (OpenTimestamps only, raw transaction reveal, or both)?
4. **Identity:** How should revocation freshness be evaluated when verifiers remain partitioned through Mars conjunction-style blackout windows ([C-026](../docs/claims.md))?
5. **Identity:** What normative fork tie-breakers are acceptable when two successors have valid signatures and no human-chosen policy exists ([Q-006](../docs/claims.md))?
6. **Space operations:** Which Bundle Protocol custody and aggregation profiles fit multi-hop Mars relay bundles without centralizing trust ([Q-011](../docs/claims.md))?
7. **Space law:** How should entities document continuing state supervision under Outer Space Treaty Article VI without implying that anchors substitute for national authorization ([C-002](../docs/claims.md))?
8. **Law:** Do existence-before Bitcoin proofs align with any trust-service or evidentiary comparators counsel would use in cross-border commercial disputes ([Q-008](../docs/claims.md))?