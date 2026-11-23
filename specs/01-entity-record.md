# Chapter 01: Signed portable entity record

Status: discussion draft. Claim labels: [00-conventions.md](00-conventions.md). Cited facts: [docs/claims.md](../docs/claims.md). Supersedes the minimum record and verification outline in [core-v0.1.md](core-v0.1.md) for normative field names and the seven-step verifier; [core-v0.1.md](core-v0.1.md) remains as a historical concept draft.

## Problem

Participants need a portable data structure that states who an economic actor claims to be, who may update that claim, and which evidence supports the claim, without requiring trust in a single operator or implying that any court or registrar accepts the claim.

**Verified fact (with source):** National and regional registries identify legal entities; GLEIF operates the global LEI system for participating jurisdictions ([GLEIF](https://www.gleif.org/) (accessed 2026-11-23), [C-009](../docs/claims.md)).

**Proposal:** UCP layer 1 (ULEI in [docs/architecture.md](../docs/architecture.md)) should begin with this signed entity record as the first interoperability milestone per [STATUS.md](../STATUS.md). The record MUST be verifiable offline from carried proof data plus Bitcoin chain data under stated assumptions, so store-and-forward and long light lag ([C-001](../docs/claims.md), [C-019](../docs/claims.md)) do not require live calls to a proprietary API.

**Verified fact (with source):** A cryptographic identifier does not confer legal personality ([docs/research/assumptions-and-corrections.md](../docs/research/assumptions-and-corrections.md)).

## Existing alternatives

### W3C Verifiable Credentials and Controlled Identifiers

**Verified fact (with source):** On 15 May 2025 the W3C Verifiable Credentials 2.0 family, including the Verifiable Credentials Data Model v2.0 and Controlled Identifiers v1.0, became W3C Recommendations ([W3C news](https://www.w3.org/news/2025/the-verifiable-credentials-2-0-family-of-specifications-is-now-a-w3c-recommendation/) (accessed 2026-11-23), [C-012](../docs/claims.md)).

**Verified fact (with source):** The VC Data Model defines machine-readable credentials and verification concepts ([W3C VC Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/) (accessed 2026-11-23), [C-008](../docs/claims.md)).

**Proposal:** UCP records MAY embed or reference W3C verifiable credentials for registration-related claims. A credential proves an issuer made a claim; it does not prove that a court accepts the claim ([docs/research/assumptions-and-corrections.md](../docs/research/assumptions-and-corrections.md)).

### GLEIF vLEI and KERI

**Verified fact (with source):** After a legal entity obtains an LEI, it may obtain a verifiable LEI (vLEI) through a Qualified vLEI Issuer ([GLEIF Get a vLEI](https://www.gleif.org/en/organizational-identity/get-an-lei-vlei/get-a-vlei) (accessed 2026-11-23), [C-013](../docs/claims.md)).

**Verified fact (with source):** The vLEI Ecosystem Governance Framework includes controlled documents for Technical Requirements Part 1: KERI Infrastructure ([GLEIF vLEI EGF](https://www.gleif.org/en/organizational-identity/become-a-vlei-issuer-qvi/vlei-ecosystem-governance-framework) (accessed 2026-11-23), [C-014](../docs/claims.md)).

**Proposal:** UCP `legalRegistrations` SHOULD be able to carry an LEI and optional vLEI credential references without requiring participation in the vLEI program.

### DID methods on Bitcoin

**Verified fact (with source):** The `did:btcr2` method specification states it is under active development and may be subject to breaking changes; publication date 20 November 2026 ([did:btcr2 specification](https://dcdpr.github.io/did-btcr2/) (accessed 2026-11-23), [C-015](../docs/claims.md)).

**Verified fact (with source):** The `decentralized-identity/ion` repository last received a default-branch push on 2023-08-25 ([GitHub ion](https://github.com/decentralized-identity/ion) (accessed 2026-11-23), [C-016](../docs/claims.md)).

**Verified fact (with source):** The `MicroStrategy/did-btc-spec` repository last received a commit on 2024-08-22 ([GitHub did-btc-spec](https://github.com/MicroStrategy/did-btc-spec) (accessed 2026-11-23), [C-017](../docs/claims.md)).

**Verified fact (with source):** Microsoft Entra Verified ID ended `did:ion` preview support in December 2023; only `did:web` remains selectable ([Microsoft FAQ](https://learn.microsoft.com/en-us/entra/verified-id/verifiable-credentials-faq) (accessed 2026-11-23), [C-006](../docs/claims.md)).

**Open question:** Whether the `did:btco` editors draft on Bitcoin ordinals inscriptions is suitable as a long-term identifier carrier; automated fetch of [BTCO DID Method](https://identity.foundation/labs-ordinals-plus/btco-did-method/) returned HTTP 403 from this environment though manual review matched an editors draft status (see [Q-007](../docs/claims.md)).

**Proposal:** UCP keeps `entityId` DID-method agnostic. DID strings MAY appear in `entityId` or in nested registration evidence, but history verification MUST NOT depend on a single DID resolver remaining online. Method migration MUST preserve a stable logical `entityId` and verifiable linkage across record versions.

### OpenTimestamps and Bitcoin anchoring

**Verified fact (with source):** OpenTimestamps states that a timestamp proves that some data existed prior to some point in time ([OpenTimestamps](https://opentimestamps.org/) (accessed 2026-11-23), [C-018](../docs/claims.md)).

**Verified fact (with source):** The `opentimestamps-client` package version 0.8.0 was published on 2026-10-27 ([PyPI](https://pypi.org/project/opentimestamps-client/) (accessed 2026-11-23), [C-020](../docs/claims.md)).

**Assumption:** Bitcoin anchoring, when used, establishes existence-before-time under verifier-chosen confirmation assumptions; it does not establish legal truth, authorship, or registrar acceptance ([docs/research/assumptions-and-corrections.md](../docs/research/assumptions-and-corrections.md)).

### Store-and-forward and light lag

**Verified fact (with source):** NASA describes Earth-to-Mars command latency between 3 and 22 minutes for the Perseverance rover depending on orbital position ([NASA Science](https://science.nasa.gov/blog/speaking-percys-language-how-to-talk-so-perseverance-will-listen/) (accessed 2026-11-23), [C-019](../docs/claims.md)).

**Verified fact (with source):** Bundle Protocol version 7 is specified in [RFC 9171](https://www.rfc-editor.org/rfc/rfc9171.html) (accessed 2026-11-23), [C-021](../docs/claims.md)).

**Proposal:** Entity record distribution MAY use delay-tolerant bundles; this chapter does not normatively profile BPv7 endpoints.

### Agent authority patterns

**Verified fact (with source):** Lightning Labs describes L402 as payment authentication for machine access, not legal identity or transaction mandate proof ([Lightning Engineering post](https://lightning.engineering/posts/2026-02-11-ln-agent-tools/) (accessed 2026-11-23), [C-022](../docs/claims.md)).

**Verified fact (with source):** Proof published the x401 protocol on 2026-10-15 as one HTTP pattern for agents to carry identity and authorization evidence ([Proof blog](https://www.proof.com/blog/proof-launches-x401-giving-ai-agents-a-way-to-prove-who-they-represent---and-what-theyre-authorized-to-do) (accessed 2026-11-23), [C-023](../docs/claims.md)).

**Proposal:** Scoped AI agent authority SHOULD be expressed as signed delegations from `authorizedKeys`, with revocation references, not as payment proofs alone.

### Space law context (non-normative)

**Verified fact (with source):** Outer Space Treaty Article VI requires state authorization and supervision of non-governmental space activities ([UNOOSA](https://www.unoosa.org/oosa/en/ourwork/spacelaw/treaties/outerspacetreaty.html) (accessed 2026-11-23), [C-002](../docs/claims.md)).

**Open question:** Whether UNCITRAL Model Law on Identity Management and Trust Services (2022) offers a useful comparator for jurisdiction-agnostic record policy; the UNCITRAL MLIT landing page returned HTTP 403 to automated fetch in this environment ([UNCITRAL MLIT](https://uncitral.un.org/en/mlit) (accessed 2026-11-23), [Q-008](../docs/claims.md)).

## Proposal

### Scope and explicit non-goals

This chapter normatively defines the **entity record** object, its minimum fields, and a seven-step verification procedure returning `valid`, `invalid`, or `indeterminate` with reasons.

This chapter explicitly does **not** specify:

- creation of legal personality or recognition as a legal person in any jurisdiction;
- issuance of securities, tokens, or protocol-native coins ([STATUS.md](../STATUS.md));
- mandatory use of Taproot Assets or RGB at layer 1 ([C-005](../docs/claims.md); later-layer only per [STATUS.md](../STATUS.md));
- universal courts, compulsory reputation scores, or interplanetary consensus ([core-v0.1.md](core-v0.1.md)).

### Document object model (normative)

An **entity record** is a single version in an append-only, hash-linked chain. Each record version MUST contain the fields in the table below. Fields use camelCase per [00-conventions.md](00-conventions.md).

| Field | Type | Normative requirements |
| --- | --- | --- |
| `protocolVersion` | string | MUST be a semantic version string per [semver.org](https://semver.org/) identifying the protocol edition this record claims to follow. Verifiers MUST reject records with an unsupported `protocolVersion` as **invalid** unless local policy explicitly allows experimental versions. |
| `entityId` | string | MUST be a stable protocol identifier for the logical entity, distinct from any official registration number. MUST remain unchanged across method migration and DID method changes. MAY be a URI. If it contains a DID, verifiers MUST NOT require live DID resolution to complete steps 1 through 5 when the record and prior chain supply sufficient key material and policy. |
| `legalRegistrations` | array of objects | SHOULD list claimed jurisdictions and official identifiers. Each element MUST include `jurisdiction` (string) and SHOULD include `officialId` (string), `evidence` (array of URIs or content digests), and optional `credential` (object or URI referencing a W3C VC). MUST NOT be interpreted as verified registration without verifier policy and primary registrar evidence. |
| `authorizedKeys` | array of objects | MUST list public keys currently authorized to sign record updates. Each element MUST include `id` (string), `publicKeyMultibase` or `publicKeyJwk` (one REQUIRED), and `role` (string). SHOULD include `validFrom` and `validUntil` as [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339) strings. MAY include `revocationRef` pointing to a revocation list or superseding record. |
| `authorityPolicy` | object | MUST state update rules. MUST include `authorizedSigners` (array of `authorizedKeys.id` strings) and `requiredSignatureCount` (positive integer). SHOULD include `recoveryPolicy` (object) describing how lost keys may be replaced. MAY include `delegationPolicy` describing scoped agent delegations (see below). |
| `documents` | array of objects | SHOULD reference governing documents by digest. Each element MUST include `digest` (string) and SHOULD include `uri`, `mediaType`, and `label`. Personal identity documents and confidential contracts MUST NOT appear inline; only digests or private URIs SHOULD be used per [core-v0.1.md](core-v0.1.md). |
| `previousRecordDigest` | string or null | MUST be the digest of the prior accepted record in the chain, using the digest algorithm named in the active signing profile, or MUST be `null` only for the genesis record of an `entityId`. MUST NOT be `null` for non-genesis records. |
| `effectiveAt` | string | MUST be an [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339) timestamp stating when the signer claims the record becomes effective. Verifiers MUST NOT treat `effectiveAt` as proof of wall-clock agreement or filing time ([00-conventions.md](00-conventions.md)). |
| `signatures` | array of objects | MUST contain one or more authorization signatures over the record. Each element MUST include `keyId` (matching `authorizedKeys.id`), `signature` (string), and `suite` (string naming the signing profile). The signed payload MUST bind all other fields except `signatures` and `anchorReceipt` once a canonical serialization is chosen ([Q-005](../docs/claims.md)). |
| `anchorReceipt` | object or null | MAY be present. If present, MUST include enough data for an independent party to verify an external commitment under a named anchoring profile (for example OpenTimestamps `.ots` metadata or a Bitcoin transaction reference). If absent, verifiers MUST skip anchoring checks without failing solely for absence. |

#### Delegation policy (informative pattern, normative when present)

When `authorityPolicy.delegationPolicy` is present:

- Each delegation object MUST include `delegateKeyId`, `scope` (machine-readable string or URI), `validFrom`, `validUntil`, and `issuerKeyId` referencing an authorized key.
- Delegations MUST be revocable via `revocationRef` on the delegate key or via a superseding record.
- Verifiers MUST NOT treat Lightning L402 payment proofs ([C-022](../docs/claims.md)) as satisfying `delegationPolicy` unless future chapters map them explicitly.

#### DID method migration (normative behavior)

When an entity changes DID method or resolver strategy:

- The new record MUST keep the same `entityId` string if continuity is claimed.
- The new record MUST reference the prior digest via `previousRecordDigest`.
- The new record SHOULD add a `documents` or `legalRegistrations.evidence` entry describing the migration intent.
- Verifiers validating history MUST accept chains where `entityId` is stable even when embedded DID strings in evidence change across versions (**proposal** until test vectors exist).

### Serialization and digests

**Open question:** Mandatory on-wire encoding remains unset per [00-conventions.md](00-conventions.md) and [Q-005](../docs/claims.md).

**Proposal (labeled):** Future interoperability SHOULD compare [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) (JCS) for JSON signing inputs against [RFC 8949](https://www.rfc-editor.org/rfc/rfc8949) Section 4.2 deterministic CBOR before selecting one binding for `signatures` and `previousRecordDigest`.

Until selection, implementers MUST NOT claim cross-vendor wire compatibility. Examples in this chapter use human-readable JSON and are not normative wire formats.

### Seven-step verification sequence (normative)

A conforming verifier MUST implement the following sequence and MUST return a result object with `status` one of `valid`, `invalid`, or `indeterminate`, and `reasons` (array of human-readable strings).

1. **Format and protocol version:** Parse the record. If required fields are missing or types violate this chapter, return **invalid** with reasons. If `protocolVersion` is unsupported, return **invalid** unless local policy allows experimental versions (then **indeterminate** with reason `unsupported protocolVersion`).

2. **Predecessor and policy:** If `previousRecordDigest` is not `null`, obtain the predecessor record. If missing, return **indeterminate** with reason `predecessor unavailable`. Resolve `authorityPolicy` from the predecessor unless the current record explicitly replaces policy per local rules; if policy cannot be resolved, return **indeterminate**.

3. **Signatures and keys:** Verify each signature in `signatures` against the signing payload under the stated `suite`, using keys listed in `authorizedKeys` for the relevant validity window. If any required signature is missing or cryptographically invalid, return **invalid**. If keys are expired or revoked per carried revocation data, return **invalid** or **indeterminate** depending on whether revocation status is definitive.

4. **Sequence and conflicts:** Confirm `previousRecordDigest` matches the digest of the obtained predecessor. If multiple successors share the same predecessor and policy does not resolve forks, return **indeterminate** with reason `competing successors` ([Q-006](../docs/claims.md)). If digest mismatch, return **invalid**.

5. **Registration evidence:** Inspect `legalRegistrations` and attached credentials without treating presence as legal recognition. Return **indeterminate** if verifier policy requires external registrar confirmation that is unavailable offline.

6. **Anchor receipt:** If `anchorReceipt` is present, verify it under the named profile and stated Bitcoin confirmation assumptions. If anchoring verification fails, return **invalid** for cryptographic failure or **indeterminate** if required chain data is temporarily unavailable. If absent, proceed without anchoring failure.

7. **Report:** If steps 1 through 4 pass and steps 5 and 6 do not yield **invalid** or blocking **indeterminate**, return **valid** with any non-blocking **indeterminate** reasons from step 5 noted. Otherwise aggregate the strongest failure.

**Note:** **indeterminate** is intentional for partitioned networks, missing predecessors, or unresolved forks so verifiers do not falsely claim **valid** when evidence is incomplete.

### Example (fictional, not normative wire format)

The following JSON uses fictional values only. It illustrates field shape; digest values, keys, and URIs are not real test vectors.

```json
{
  "protocolVersion": "0.1.0",
  "entityId": "ucp:entity:fictional-orbit-trading-collective",
  "legalRegistrations": [
    {
      "jurisdiction": "EX-FICT",
      "officialId": "FICT-0000-0000",
      "evidence": ["ipfs://bafy-fictional-example-cid"]
    }
  ],
  "authorizedKeys": [
    {
      "id": "key-fict-01",
      "publicKeyMultibase": "z6Mk-fictional-example-key-material-only",
      "role": "administrator",
      "validFrom": "2026-01-01T00:00:00Z"
    }
  ],
  "authorityPolicy": {
    "authorizedSigners": ["key-fict-01"],
    "requiredSignatureCount": 1,
    "recoveryPolicy": {
      "description": "Fictional social recovery requiring two-of-three custodians"
    }
  },
  "documents": [
    {
      "label": "Fictional operating agreement digest",
      "digest": "sha256:fictionalhexdigest000000000000000000000000000000000000000000000000",
      "mediaType": "application/pdf"
    }
  ],
  "previousRecordDigest": null,
  "effectiveAt": "2026-06-15T12:00:00Z",
  "signatures": [
    {
      "keyId": "key-fict-01",
      "suite": "fictional-suite-pending-selection",
      "signature": "fictional-signature-bytes"
    }
  ],
  "anchorReceipt": null
}
```

## Trust assumptions

- Verifiers possess correct implementations of chosen cryptographic suites once standardized.
- Predecessor records and revocation lists are available when verifying non-genesis updates, or the verifier honestly reports **indeterminate**.
- Bitcoin full nodes or equivalent data sources are available when verifying `anchorReceipt` under OpenTimestamps or custom anchoring profiles ([C-018](../docs/claims.md)).
- Participants do not treat **valid** verification as legal recognition, securities compliance, or registrar confirmation.

## Legal implications

This chapter does **not** claim that conforming records create legal persons, bind third parties, satisfy KYC or AML rules, or replace statutory registers.

**Verified fact (with source):** States bear responsibility under the Outer Space Treaty for authorizing and supervising non-governmental space activities ([C-002](../docs/claims.md)). Portable records do not remove that obligation.

Unsettled items belong in Open questions and qualified legal review. No enforcement mechanism is specified here.

## Privacy impact

- Public records SHOULD minimize personal data; only digests or references SHOULD appear in `documents` and `legalRegistrations.evidence`.
- `effectiveAt`, keys, and registration claims reveal organizational metadata; operators SHOULD assess GDPR and other regimes before publishing.
- OpenTimestamps calendars learn digests of stamped material; operators SHOULD understand calendar privacy properties ([OpenTimestamps](https://opentimestamps.org/) (accessed 2026-11-23)).

## Verification method

Independent conformance review MUST:

1. Apply the seven-step sequence to official test vectors once published.
2. Confirm field tables match instances under test.
3. Confirm **indeterminate** is returned when predecessors or registrar evidence is withheld.
4. Confirm examples are labeled fictional and are not used as wire format conformance data.

## Smallest useful test

Apply the chapter 00 pull request checklist from [00-conventions.md](00-conventions.md#smallest-useful-test) to this file.

Minimal falsification experiment for chapter 01:

1. Publish two successor records sharing the same `previousRecordDigest` and demonstrate the verifier returns **indeterminate** with reason `competing successors`.
2. Mutate one signed field after signing and demonstrate step 3 returns **invalid**.
3. Provide a complete OpenTimestamps proof for a record digest, stamp it, upgrade per client documentation, and demonstrate step 6 returns **valid** under a documented confirmation depth assumption.
4. Remove the predecessor record from the bundle and demonstrate step 2 returns **indeterminate**.

## Open questions

1. **Identity (external experts):** Which combination of LEI, vLEI credentials ([C-013](../docs/claims.md)), and portable `entityId` strings should pilots require so registrars and counterparties can map records without locking to one DID method?
2. **Identity:** What minimum `delegationPolicy` fields should lawyers and auditors accept as evidence of human authorization for high-consequence agent actions, distinct from payment authentication ([C-022](../docs/claims.md), [C-023](../docs/claims.md))?
3. **Bitcoin timestamping:** Should `anchorReceipt` normatively profile OpenTimestamps only, raw Bitcoin transactions, or both, and what confirmation depth satisfies **valid** for high-value updates ([Q-009](../docs/claims.md))?
4. **Bitcoin timestamping:** When incomplete OTS proofs depend on calendar servers, MUST verifiers require `ots upgrade` completion before **valid**, and how should that interact with offline verification goals?
5. **Serialization:** Should UCP adopt JCS, deterministic CBOR, or another ruleset for signing inputs ([Q-005](../docs/claims.md))?
6. **Fork resolution:** What normative tie-breakers should apply when two signed successors exist ([Q-006](../docs/claims.md))?
7. **Space law:** How should entities operating in outer space document state authorization and supervision obligations under Outer Space Treaty Article VI ([C-002](../docs/claims.md)) without implying the record itself satisfies national licensing?
8. **Comparators:** Does UNCITRAL MLIT (2022) define trust-service concepts that should align with `authorityPolicy` ([Q-008](../docs/claims.md))?