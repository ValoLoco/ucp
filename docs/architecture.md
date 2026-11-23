# UCP Architecture v0.1

> **Proposal:** This document maps long-term problems and candidate mechanisms. It is not a deployment specification. For project status, read [STATUS.md](../STATUS.md). For claim labels, read [specs/00-conventions.md](../specs/00-conventions.md). The [claims register](claims.md) lists cited facts.

## Problem

**Verified fact (with source):** Legal entities are identified and governed through national and regional registries; the global LEI system ties identifiers to legal entities in participating jurisdictions ([GLEIF](https://www.gleif.org/) (accessed 2026-11-23)).

**Proposal:** As commerce may extend into orbit and beyond, participants may need portable identity, ownership records, contracts, dispute resolution, reputation, settlement, and governance patterns that interoperate across venues. None of that is implemented by UCP today.

## Research context (cited)

**Verified fact (with source):** One-way Earth-Mars light time ranges from about 3 minutes to about 22.4 minutes depending on orbital position ([NASA Mars Relay Network](https://science.nasa.gov/mars/mars-relay-network/) (accessed 2026-11-23)).

**Verified fact (with source):** Under the Outer Space Treaty Article VI, states bear international responsibility for national activities in outer space and must authorize and supervise non-governmental entities ([UNOOSA Outer Space Treaty](https://www.unoosa.org/oosa/en/ourwork/spacelaw/treaties/outerspacetreaty.html) (accessed 2026-11-23)).

**Verified fact (with source):** As of 2026-10-28, NASA reports that Vietnam became the 78th nation to sign the Artemis Accords, which articulate principles for civil lunar and space exploration and reference the Outer Space Treaty ([NASA Artemis Accords](https://www.nasa.gov/artemis-accords/) (accessed 2026-11-23)).

**Proposal:** A "Starlink-style" commercial Mars relay constellation dedicated to general interplanetary commerce is not described as an existing service in authoritative NASA Mars relay documentation; any similar idea for company protocols would be greenfield engineering on top of today's government and interagency relay models ([C-001](claims.md#claims-and-sources)).

## Stack (proposal map)

```text
L7 Algorithmic Governance Framework
L6 Interstellar Settlement Layer
L5 Universal Reputation Ledger
L4 Interstellar Commercial Court
L3 Universal Commercial Code
L2 Universal Capital Table
L1 Universal Legal Entity Identifier

Bitcoin L1: consensus, timestamping, finality (Assumption: optional anchor layer)
```

**Proposal:** Layer names describe problem areas, not shipped products. Bitcoin L1 is under evaluation as a neutral commitment layer, not a requirement for the first demonstrator.

## Layer specifications

Each subsection below mixes **proposal** and **assumption** items. They do not imply legal recognition, court enforcement, or production readiness.

### L1: ULEI

- **Assumption:** Entity identity may use W3C Verifiable Credentials for legal-entity and registration-related claims ([W3C VC Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/) (accessed 2026-11-23)).
- **Proposal:** Compare DID methods (`did:web`, `did:key`, and others). **`did:ion` is not a default recommendation:** Microsoft Entra Verified ID supported `did:ion` in preview until December 2023 and now documents migration to `did:web` ([Microsoft FAQ](https://learn.microsoft.com/en-us/entra/verified-id/verifiable-credentials-faq) (accessed 2026-11-23)).
- **Assumption:** A registrar bridge (for example a smart contract on an adjacent chain) could map a protocol entity identifier to credentials and jurisdiction hints.
- **Assumption:** Periodic Merkle roots of credential commitments might anchor to Bitcoin via `OP_RETURN` or similar mechanisms if a pilot justifies the cost.

### L2: UCT

- **Verified fact (with source):** Taproot Assets is alpha software; Lightning Labs states to use mainnet at your own risk ([get-tapd](https://docs.lightning.engineering/lightning-network-tools/taproot-assets/get-tapd) (accessed 2026-11-23)).
- **Proposal:** Taproot Assets universes might model share classes or other instruments only under applicable securities law and with qualified review.
- **Assumption:** Contract logic on an adjacent chain (for example Clarity on Stacks) could encode transfer rules if requirements exceed offline records.
- **Proposal:** Off-chain KYC and AML validators might co-sign permitted transfers; this does not replace legal registers.

### L3: UCC-X

- **Proposal:** Template library (SAFE, SPA, services agreement, offtake, joint venture) as machine-readable drafts, not automatic law.
- **Assumption:** On-chain execution on an adjacent chain with decidable logic if parties contractually adopt it.
- **Assumption:** Light-lag buffers using block height and timestamps informed by **C-001**; interplanetary suitability is an **Open question** ([claims.md](claims.md)).

### L4: ICC-X

- **Proposal:** Dispute workflows with Bitcoin-anchored transcripts and Merkle commitments as evidence, not as a substitute for national courts.
- **Assumption:** Arbitration orchestration via smart contracts if parties opt into recognized arbitration rules ([UNCITRAL texts](https://uncitral.un.org/en/texts/arbitration) (accessed 2026-11-23)).
- **Proposal:** Enforcement would remain jurisdiction-dependent; registrars or courts would need to accept outcomes under existing law.
- **Assumption:** BitVM-style verification might assist high-value technical disputes; it would not replace due process (**Open question:** maturity and fit).

### L5: URL

- **Proposal:** Attestations for KYC, audits, insurance, delivery, and dispute outcomes as verifiable credentials.
- **Assumption:** Content addressing (IPFS, Arweave, or similar) with Merkle roots anchored to Bitcoin if needed.
- **Assumption:** Verification via DID resolution and read-only chain queries.

### L6: ISL

- **Assumption:** Lightning, Taproot Assets on Lightning, or swaps might support fast settlement where legally permitted and technically viable.
- **Open question:** HTLC timelocks and channel monitoring under Earth-Mars light lag (**C-001**); Lightning is not presumed suitable for interplanetary settlement (see [assumptions-and-corrections.md](research/assumptions-and-corrections.md)).

### L7: AGF

- **Proposal:** Governance proposals, voting, timelocks, and treasury controls as explicit rules where law allows.
- **Assumption:** Fiduciary rules partially encoded as assertions; full duties remain off-chain and legal.
- **Proposal:** AI agents receive scoped, revocable authority through capability credentials; legal personality is **not** proposed for v1.

## Roadmap (ideation)

**Proposal:** Possible expansion phases, not scheduled commits:

1. Protocol definition and reference implementations.
2. Orbital MVP concepts spanning multiple layers if review supports them.
3. Cis-lunar extension: light-lag-aware contracts, resource title ideas, parametric insurance concepts.
4. Interplanetary extension: relativistic timelocks, extraterrestrial incorporation scenarios, identity infrastructure scenarios.

## Open questions

- Which registrar jurisdictions should participate first? (**Open question**)
- Should a future UCT experiment use Taproot Assets or RGB? (**Open question**)
- Should ICC-X start with adjacent-chain logic and later add BitVM-style paths? (**Open question**)
- Should AI-agent legal personality be included in v1 or deferred? (**Open question** per [core-v0.1.md](../specs/core-v0.1.md))
- How should UCP be funded without a protocol token? (**Open question**)