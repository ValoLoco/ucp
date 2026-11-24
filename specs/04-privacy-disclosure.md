# Chapter 04: Privacy and disclosure

Status: discussion draft. Claim labels: [00-conventions.md](00-conventions.md). Cited facts: [docs/claims.md](../docs/claims.md). Builds on [01-entity-record.md](01-entity-record.md) (record fields, seven-step verifier), [02-entity-history.md](02-entity-history.md) (public anchors, bundle minimization), and [03-verification.md](03-verification.md) (outcomes, `reasonCodes`, offline behavior). This chapter does not select serialization, digest algorithm, or signature suite ([Q-005](../docs/claims.md)).

## Problem

Entity records and their histories carry organizational claims, registration evidence, authorized keys, governing document digests, and optional anchor receipts. Participants need clear rules for which parts of that data are public, which stay off public records and anchors, how selective disclosure of registration evidence and documents works through digest commitments and holder-presented evidence, what a verifier can still check when content is withheld, correlation risks of public anchors and stable identifiers, key and signer privacy, data minimization and retention, and how these interact with offline and light-lag verification.

**Verified fact (with source):** Chapter 01 requires that personal identity documents and confidential contracts stay outside public records and public anchors, with only digests or private URIs in the `documents` array ([01-entity-record.md](01-entity-record.md)).

**Verified fact (with source):** Chapter 02 states that public anchors SHOULD carry digests only and that rich metadata in records remains off-chain by default ([02-entity-history.md](02-entity-history.md) Privacy impact).

**Proposal:** This chapter normatively defines privacy and disclosure rules for UCP entity records and histories, reusing field names, verification outcomes (`valid`, `invalid`, `indeterminate`), and machine-readable `reasonCodes` from [03-verification.md](03-verification.md) without contradicting chapter 01 steps or chapter 03 Phases A through E.

## Existing alternatives

### W3C Verifiable Credentials selective disclosure

**Verified fact (with source):** On 15 May 2025 the W3C Verifiable Credentials 2.0 family, including the Verifiable Credentials Data Model v2.0, became W3C Recommendations ([W3C news](https://www.w3.org/news/2025/the-verifiable-credentials-2-0-family-of-specifications-is-now-a-w3c-recommendation/) (accessed 2026-11-24), [C-012](../docs/claims.md)).

**Verified fact (with source):** The VC Data Model defines machine-readable credentials and verification concepts ([W3C VC Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/) (accessed 2026-11-24), [C-008](../docs/claims.md)).

**Verified fact (with source):** The VC Data Model describes selective disclosure of credential properties by the holder to a verifier, including derived credentials formatted to a verifier schema without issuer involvement at presentation time ([W3C VC Data Model 2.0 selective disclosure](https://www.w3.org/TR/vc-data-model-2.0/#zero-knowledge-proofs) (accessed 2026-11-24), [C-029](../docs/claims.md)).

**Proposal:** UCP MAY reference W3C VC selective disclosure mechanisms for registration evidence in `legalRegistrations.evidence` or embedded credentials. History verification MUST NOT depend on a specific VC format, zero-knowledge suite, or resolver remaining online ([03-verification.md](03-verification.md)).

### GLEIF vLEI and KERI controlled disclosure

**Verified fact (with source):** After a legal entity obtains an LEI, it may obtain a verifiable LEI (vLEI) through a Qualified vLEI Issuer ([GLEIF Get a vLEI](https://www.gleif.org/en/organizational-identity/get-an-lei-vlei/get-a-vlei) (accessed 2026-11-24), [C-013](../docs/claims.md)).

**Verified fact (with source):** The vLEI Ecosystem Governance Framework includes controlled documents for Technical Requirements Part 1: KERI Infrastructure ([GLEIF vLEI EGF](https://www.gleif.org/en/organizational-identity/become-a-vlei-issuer-qvi/vlei-ecosystem-governance-framework) (accessed 2026-11-24), [C-014](../docs/claims.md)).

**Proposal:** UCP `legalRegistrations` SHOULD be able to carry LEI and optional vLEI credential references without requiring participation in the vLEI program, and without forcing public disclosure of full credential payloads.

### OpenTimestamps calendar privacy

**Verified fact (with source):** OpenTimestamps states that a timestamp proves that some data existed prior to some point in time ([OpenTimestamps](https://opentimestamps.org/) (accessed 2026-11-24), [C-018](../docs/claims.md)).

**Verified fact (with source):** The OpenTimestamps site documents free-to-use calendar servers that perform stamping on behalf of users and do not require registration ([OpenTimestamps](https://opentimestamps.org/) (accessed 2026-11-24), [C-027](../docs/claims.md)).

**Verified fact (with source):** The OpenTimestamps client README documents submitting stamp requests to remote calendar servers when creating a timestamp ([OpenTimestamps client README](https://github.com/opentimestamps/opentimestamps-client/blob/master/README.md) (accessed 2026-11-24), [C-030](../docs/claims.md)).

**Assumption:** Calendar operators learn the digest (or preimage) presented at stamp time. Operators SHOULD treat calendar submission as a disclosure event, consistent with chapter 02 ([02-entity-history.md](02-entity-history.md) Privacy and public anchors).

### DID method privacy considerations

**Verified fact (with source):** The `did:btcr2` method specification states it is under active development and may be subject to breaking changes ([did:btcr2 specification](https://dcdpr.github.io/did-btcr2/) (accessed 2026-11-24), [C-015](../docs/claims.md)).

**Verified fact (with source):** The `decentralized-identity/ion` repository last received a default-branch push on 2023-08-25 ([GitHub ion](https://github.com/decentralized-identity/ion) (accessed 2026-11-24), [C-016](../docs/claims.md)).

**Proposal:** UCP keeps `entityId` DID-method agnostic. History verification MUST NOT depend on a single DID resolver remaining online. Method migration MUST preserve a stable logical `entityId` and verifiable linkage across record versions ([01-entity-record.md](01-entity-record.md)).

### Store-and-forward and light-lag constraints

**Verified fact (with source):** NASA describes Earth-to-Mars command latency between 3 and 22 minutes for the Perseverance rover depending on orbital position ([NASA Science](https://science.nasa.gov/blog/speaking-percys-language-how-to-talk-so-perseverance-will-listen/) (accessed 2026-11-24), [C-019](../docs/claims.md)).

**Verified fact (with source):** A NASA Moon to Mars architecture white paper states that direct spacecraft-to-Earth communications blackouts are inevitable and can last weeks, on the order of 13 to 21 days for representative mission profiles ([NASA Mars communications disruption and delay PDF](https://www.nasa.gov/wp-content/uploads/2024/01/mars-communications-disruption-and-delay.pdf) (accessed 2026-11-24), [C-026](../docs/claims.md)).

**Verified fact (with source):** Bundle Protocol version 7 is specified in [RFC 9171](https://www.rfc-editor.org/rfc/rfc9171.html) (accessed 2026-11-24), [C-021](../docs/claims.md)).

**Proposal:** Privacy rules MUST accommodate offline and light-lag verification where verifiers cannot reach live registrars or calendars, and MUST return `indeterminate` honestly when evidence is withheld or unavailable per chapter 03 aggregation ([03-verification.md](03-verification.md) Phase E).

## Proposal

### Public versus private fields (normative)

The following entity record fields from [01-entity-record.md](01-entity-record.md) MAY appear in public records and, when applicable, in public anchor commitments:

- `protocolVersion`
- `entityId`
- `previousRecordDigest`
- `anchorReceipt` (digest commitment and proof metadata only; see [02-entity-history.md](02-entity-history.md) Privacy and public anchors)
- `signatures` (signature values, `keyId`, and `suite` identifiers)
- `effectiveAt` (claimed time only; [00-conventions.md](00-conventions.md))

The following fields MUST NOT appear in public anchors. They MAY appear in public records at the entity's discretion, but operators SHOULD minimize their publication in widely replicated bundles ([02-entity-history.md](02-entity-history.md)):

- `legalRegistrations` (jurisdiction claims, official identifiers, evidence references, credential references)
- `authorizedKeys` (public key material, roles, validity windows, `revocationRef`)
- `authorityPolicy` (update rules, recovery policy, delegation policy)
- `documents` (governing document digests, labels, media types, URIs)

Personal identity documents and confidential contracts MUST NOT appear inline in any record; only digests or private URIs SHOULD be used per [01-entity-record.md](01-entity-record.md) and [core-v0.1.md](core-v0.1.md). Full records MUST stay off public anchors unless the entity explicitly accepts the privacy risk ([02-entity-history.md](02-entity-history.md)).

### Selective disclosure of registration evidence and documents (normative)

When `legalRegistrations.evidence` or `documents` entries use content digests (for example `sha256:hex...`) or private URIs, the holder MAY present the full content to a specific verifier off-band.

**Verified fact (with source):** Chapter 01 step 5 inspects `legalRegistrations` and attached credentials without treating presence as legal recognition ([01-entity-record.md](01-entity-record.md)).

**Proposal:** A verifier receiving holder-presented bytes for a digest-backed reference MUST verify that the presented content matches the committed digest in the record under the active digest profile ([Q-005](../docs/claims.md)). If the content matches, the verifier MAY evaluate the evidence under verifier policy. If the content does not match, the verifier MUST return `invalid` with `reasonCodes` containing `digest-mismatch` and a human `reasons` entry describing committed-content failure ([03-verification.md](03-verification.md)). If the holder withholds content that verifier policy requires, the verifier MUST treat step 5 as blocking `indeterminate` with proposed code `evidence-withheld` and human reason `evidence withheld`. If required content cannot be obtained for reasons other than holder refusal (for example unreachable private URI), the verifier MUST use proposed code `evidence-unavailable` and human reason `evidence unavailable`.

**Proposal:** Selectively disclosed W3C verifiable credentials MAY satisfy step 5 under verifier policy without publishing full credential bytes in the bundle ([C-029](../docs/claims.md)). Credential verification MUST remain separate from legal recognition ([03-verification.md](03-verification.md)).

### Verifier checks when content is withheld (normative)

When a holder withholds `legalRegistrations` evidence, `documents` content, or full credential payloads:

1. The verifier MUST still complete chapter 01 steps 1 through 4 (format, predecessor and policy, signatures and keys, sequence and conflicts) and chapter 03 Phases B and C for history verification when applicable.
2. For step 5, if verifier policy requires holder-presented or registrar-backed content that is not supplied:
   - Withholder refusal: blocking `indeterminate` with `evidence-withheld` (proposal; integrates with [03-verification.md](03-verification.md) Phase E item 2).
   - External registrar confirmation required but offline: `registrar-confirmation-unavailable` as blocking or non-blocking per existing verifier policy ([03-verification.md](03-verification.md) Proposed reason codes table).
   - Unreachable evidence location: blocking `indeterminate` with `evidence-unavailable` (proposal).
3. The verifier MUST still process `anchorReceipt` when present (chapter 01 step 6; chapter 03 Phase D). Missing Bitcoin chain data MUST yield `anchor-data-unavailable` or warnings per `allowProvisionalAnchors` ([03-verification.md](03-verification.md)), not substitution for step 5 failures.
4. The chain `status` MUST follow chapter 03 Phase E: any `invalid` from steps 1 through 4 or digest mismatch dominates; otherwise blocking `indeterminate` when required evidence is withheld; otherwise `valid` with applicable `warnings`.

This allows counterparties to confirm chain integrity, signature validity, and anchoring while deferring registration evidence evaluation.

### Proposed privacy reason codes (extension to chapter 03)

The following codes are **proposal** until bundled with chapter 03 normative stability ([Q-012](../docs/claims.md), [Q-018](../docs/claims.md)). They use the same lowercase hyphen style as [03-verification.md](03-verification.md).

| Code | Typical `status` | Use |
| --- | --- | --- |
| `evidence-withheld` | indeterminate (blocking when policy requires content) | Holder refused to present digest-backed content |
| `evidence-unavailable` | indeterminate (blocking when policy requires content) | Content not obtainable (network, expiry, missing URI access) |

Existing chapter 03 codes used by this chapter include `digest-mismatch`, `registrar-confirmation-unavailable`, `anchor-data-unavailable`, `anchor-confirmations-unverified`, and `revocation-data-missing` ([03-verification.md](03-verification.md)).

### Correlation risks of public anchors and stable identifiers (normative)

**Proposal:** Entities SHOULD assess correlation risks before publishing:

- A stable `entityId` across records enables linking all versions of an entity history by any observer.
- Public `anchorReceipt` values that commit the same record digest or `entityId` to Bitcoin create a public timestamped linkage.
- `authorizedKeys` public key material, if published, enables linking signatures across records and external systems.
- `legalRegistrations.officialId` values (for example LEI) create direct correlation with registrar databases.

Operators SHOULD minimize fields published in widely replicated bundles ([02-entity-history.md](02-entity-history.md)). When correlation risk is unacceptable, entities MAY:

- Use distinct `entityId` values for distinct operational contexts, with a verifiable linkage proof if continuity must be proven later.
- Omit `legalRegistrations.officialId` from public records and provide it only via holder-presented evidence.
- Rotate `authorizedKeys` on a schedule that limits linkability, with `revocationRef` pointing to superseding records.
- Avoid reusing the same digest commitment across unrelated anchor receipts.

### Key and signer privacy (normative)

**Proposal:** Public key material in `authorizedKeys` reveals organizational metadata (key types, rotation patterns, role assignments). Operators SHOULD assess GDPR and other data-protection regimes before publishing ([01-entity-record.md](01-entity-record.md) Privacy impact). This chapter does **not** claim that GDPR, CCPA, Example Jurisdiction law, or any other regime applies or does not apply; such questions are open ([Q-024](../docs/claims.md)).

When `authorityPolicy.delegationPolicy` is present, delegation objects include `delegateKeyId`, `scope`, `validFrom`, `validUntil`, and `issuerKeyId` ([01-entity-record.md](01-entity-record.md)). Publishing delegations reveals agent scopes and issuer-delegate relationships. Operators SHOULD consider publishing only delegation digests in public records and providing full delegation objects via holder-presented evidence.

### Data minimization and retention (normative)

**Proposal:** Records and histories SHOULD include only fields necessary for the claimed purpose. `documents` arrays SHOULD reference governing documents by digest only, with optional `uri`, `mediaType`, and `label`. `legalRegistrations.evidence` SHOULD use digests or private URIs rather than inline credential payloads.

Retention of off-band evidence (full documents, credentials, registration proofs) is a local policy matter. Verifiers MUST NOT assume off-band evidence remains available indefinitely. If evidence becomes unavailable, verification returns `indeterminate` with `evidence-unavailable` when policy requires that evidence, per rules above.

### Offline and light-lag verification interaction (normative)

**Assumption:** Verifiers in disconnected or high-latency environments ([C-019](../docs/claims.md), [C-026](../docs/claims.md)) operate on bundles received via store-and-forward transport ([C-021](../docs/claims.md)) and MAY receive Bitcoin blocks asynchronously ([C-025](../docs/claims.md)).

**Proposal:** Under long one-way delays or multi-week Earth-Mars communications blackout windows ([C-026](../docs/claims.md)), operators SHOULD plan for autonomous issuance and verification with cached keys, local bundles, and optional satellite-received Bitcoin blocks ([C-025](../docs/claims.md)).

When verifiers are partitioned:

- They MUST complete chapter 01 steps 1 through 4 using carried proof data.
- They MUST apply chapter 03 offline rules for revocation staleness and provisional anchors ([03-verification.md](03-verification.md) Offline and light-lag verification).
- They MUST return blocking `indeterminate` for step 5 when required evidence is withheld (`evidence-withheld`) or unreachable (`evidence-unavailable`, or `registrar-confirmation-unavailable` when blocking).
- They MUST verify `anchorReceipt` when required Bitcoin headers are available locally; otherwise return `indeterminate` or `warnings` with `anchor-data-unavailable` or `anchor-confirmations-unverified` per policy, not `invalid`.
- They MUST NOT treat `indeterminate` outcomes as `invalid` or `valid`.

## Trust assumptions

- Verifiers possess correct implementations of chosen cryptographic suites once standardized.
- Predecessor records and revocation material are available when verifying non-genesis updates, or verifiers honestly report `indeterminate` ([03-verification.md](03-verification.md)).
- Bitcoin anchoring assumes honest-majority proof-of-work chain selection and verifier-chosen confirmation depth (**assumption**, [02-entity-history.md](02-entity-history.md)).
- Calendar servers used at stamp time are not trusted for long-term verification once proofs are upgraded (**assumption**, [C-028](../docs/claims.md)).
- Holder-presented evidence matches the committed digest when supplied; verifiers check this match before policy evaluation.
- Entities assess their own correlation risks and data-protection obligations; this chapter provides no legal safe harbor.

## Legal implications

This chapter does not claim that conforming privacy practices create legal safe harbors, satisfy data-protection laws, bind third parties, or replace statutory registers.

**Verified fact (with source):** States bear responsibility under the Outer Space Treaty for authorizing and supervising non-governmental space activities ([C-002](../docs/claims.md)). Portable records do not remove that obligation.

**Verified fact (with source):** [STATUS.md](../STATUS.md) states that no participating jurisdictions, endorsements, or legal recognition are claimed for UCP.

Whether selective disclosure mechanisms affect evidentiary weight, KYC or AML compliance, registrar acceptance, or supervised space operations is an open question for qualified counsel and domain experts. No legal effect in this chapter is labeled verified fact.

## Privacy impact

- Public records SHOULD minimize personal data; only digests or references SHOULD appear in `documents` and `legalRegistrations.evidence` ([01-entity-record.md](01-entity-record.md)).
- `effectiveAt`, keys, and registration claims reveal organizational metadata; operators SHOULD assess GDPR and other regimes before publishing ([01-entity-record.md](01-entity-record.md)). Applicability of any regime is unsettled ([Q-024](../docs/claims.md)).
- OpenTimestamps calendars receive stamp submissions ([C-030](../docs/claims.md)); operators SHOULD understand calendar privacy properties ([C-018](../docs/claims.md), [02-entity-history.md](02-entity-history.md)).
- History traversal reveals update frequency, key rotation, and registration claims; operators SHOULD minimize fields published in widely replicated bundles ([02-entity-history.md](02-entity-history.md)).
- Forks reveal dispute or partition events; parties SHOULD anticipate that competing successors become visible to anyone holding the bundle ([02-entity-history.md](02-entity-history.md)).
- Correlation of `entityId` across records, anchors, and external systems enables long-term profiling; entities SHOULD assess this risk before publishing stable identifiers.

## Verification method

Independent conformance review MUST:

1. Apply chapter 01 and chapter 03 verification to records with withheld evidence and confirm blocking `indeterminate` with `evidence-withheld` or `evidence-unavailable` when policy requires content, and `registrar-confirmation-unavailable` when registrar confirmation is required but offline.
2. Confirm that public anchors carry only digests or Merkle roots, not full records, personal documents, or confidential contracts ([02-entity-history.md](02-entity-history.md)).
3. Verify that holder-presented evidence is checked against the committed digest and that mismatches yield `invalid` with `digest-mismatch`.
4. Confirm that offline verification returns `indeterminate` or `valid` with `warnings` per chapter 03 policy, not false `invalid` or `valid`, when registrar evidence or chain data is incomplete.
5. Confirm examples are labeled fictional and use **Example Jurisdiction** only.

## Smallest useful test

Apply the chapter 00 pull request checklist from [00-conventions.md](00-conventions.md#smallest-useful-test) to this file.

Minimal falsification experiments:

1. Publish a record with a `documents` entry containing only a digest and a private URI. Withhold the document content. Run the verifier with policy requiring content and confirm `indeterminate` with `evidence-withheld` while steps 1 through 4 pass.
2. Present holder-provided content that matches the committed digest. Confirm the verifier evaluates the content under verifier policy without `digest-mismatch`.
3. Present holder-provided content that does not match the committed digest. Confirm `invalid` with `digest-mismatch`.
4. Publish an `anchorReceipt` committing only the record digest. Confirm no full record fields appear in the anchor proof.
5. Simulate a partitioned verifier with local Bitcoin headers but no Internet access. Confirm anchor verification per `allowProvisionalAnchors` and `indeterminate` or `warnings` for withheld registrar evidence, not false `invalid`.
6. Publish two records with the same `entityId` but different `authorizedKeys` public key material. Confirm an observer can correlate the keys across records, demonstrating the correlation risk.

## Open questions

1. **Privacy engineering (external experts):** What selective disclosure credential formats (for example W3C VC with BBS cryptosuites, SD-JWT, or zero-knowledge proofs) should UCP profile for `legalRegistrations` credentials so verifiers can check commitments without learning full credential content, and how should revocation of selectively disclosed credentials work offline ([Q-019](../docs/claims.md), [C-029](../docs/claims.md))?

2. **Privacy engineering (external experts):** Should UCP define a normative minimal public record profile that omits `legalRegistrations`, `authorizedKeys`, `authorityPolicy`, and `documents` entirely from public bundles, requiring holder presentation for those fields, and what are the interoperability costs ([Q-020](../docs/claims.md))?

3. **Identity (external experts):** How should entities manage `entityId` correlation across operational contexts (for example Earth operations versus Mars operations) when continuity proofs are needed later, and what verifiable linkage mechanisms minimize linkability during normal operation ([Q-021](../docs/claims.md))?

4. **Bitcoin (external experts):** What anchor receipt profiles minimize metadata leakage to calendar servers and Bitcoin observers while still providing offline-verifiable existence-before evidence under Mars blackout constraints ([Q-022](../docs/claims.md), [C-030](../docs/claims.md))?

5. **Bitcoin (external experts):** Should UCP require or recommend distinct anchor commitment structures per record to prevent linkability of anchor timing across records, and how does this interact with OpenTimestamps calendar aggregation ([Q-023](../docs/claims.md))?

6. **Law (external experts):** Does any data-protection regime treat a stable `entityId` linked to public key material and anchor receipts as personal data when the entity is a legal person, and what compliance implications follow for operators who publish such records ([Q-024](../docs/claims.md))? This chapter does not answer that question.

7. **Verification (external experts):** Should `evidence-withheld` and `evidence-unavailable` merge into chapter 03 normative reason codes in the next minor version, and when MUST each be blocking versus warning ([Q-018](../docs/claims.md), [Q-012](../docs/claims.md))?

8. **Privacy engineering (external experts):** What data minimization metrics (field count, entropy of published keys, correlation surface area) should conformance suites measure so implementations do not over-publish by default ([Q-025](../docs/claims.md))?