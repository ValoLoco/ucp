# Chapter 05: Later-layer research topics

Status: discussion draft (research index, non-normative). Claim labels: [00-conventions.md](00-conventions.md). Cited facts: [docs/claims.md](../docs/claims.md). Builds on [01-entity-record.md](01-entity-record.md), [02-entity-history.md](02-entity-history.md), [03-verification.md](03-verification.md), and [04-privacy-disclosure.md](04-privacy-disclosure.md).

**Non-normative scope:** This chapter does not use [BCP 14](https://www.rfc-editor.org/info/bcp14) requirement keywords. No token, security, legal personality, or court recognition is claimed for UCP.

## How this chapter uses the template

Normative chapters follow [_template.md](_template.md): Problem, Existing alternatives, Proposal, Trust assumptions, Legal implications, Privacy impact, Verification method, Smallest useful test, and Open questions. Chapter 05 is a **research index** only ([README.md](README.md#chapter-05-scope-research-only)). Each topic below uses **Problem** and **Existing alternatives**, adds **Dependencies on chapters 01 to 04**, **What must be true before a normative chapter is justified**, and **Open questions for named kinds of experts**. Trust, legal, privacy, and verification concerns appear inside those sections rather than as repeated template headings.

**Proposal:** Future numbered chapters MAY spin out individual topics if the justification criteria are met. Layer naming (website UCP-* labels versus repository acronyms) remains unsettled per [README.md](README.md#open-questions) and [00-conventions.md](00-conventions.md); this chapter does not resolve it.

---

## 1. Universal Capital Table

### Problem

A portable capital table would record ownership, transfer restrictions, and voting rights without relying on a single jurisdictional registrar. **Open question:** Whether any Bitcoin-anchored asset layer can function as a legally effective share register under a recognized securities framework without a traditional transfer agent ([Q-026](../docs/claims.md)).

### Existing standards or projects to evaluate first

**Verified fact (with source):** Lightning Labs announced Taproot Assets v0.8 on 23 June 2026, describing mainnet multi-asset Lightning issuance and transfer ([Lightning Engineering post](https://lightning.engineering/posts/2026-06-23-tapd-0.8-launch/) (accessed 2026-11-24), [C-031](../docs/claims.md)).

**Verified fact (with source):** Taproot Assets remains alpha software; Lightning Labs warns operators to use mainnet at their own risk ([Get tapd](https://docs.lightning.engineering/lightning-network-tools/taproot-assets/get-tapd) (accessed 2026-11-24), [C-005](../docs/claims.md)).

**Verified fact (with source):** The RGB Protocol Association announced RGB v0.11.1 on Bitcoin mainnet on 17 July 2025 ([RGB mainnet launch](https://rgbprotocol.org/rgb-v0-11-1-mainnet-launch/) (accessed 2026-11-24), [C-032](../docs/claims.md)).

**Verified fact (with source):** The same announcement describes client-side validation and states there are no validators or coordinators ([RGB mainnet launch](https://rgbprotocol.org/rgb-v0-11-1-mainnet-launch/) (accessed 2026-11-24), [C-035](../docs/claims.md)).

**Verified fact (with source):** Ark Labs opened Arkade to the public on 20 October 2025 and states Arkade is not ready to handle life savings ([Ark Labs post](https://arklabs.xyz/insights/press-start-arkade-goes-live/) (accessed 2026-11-24), [C-033](../docs/claims.md)).

**Verified fact (with source):** BitVM describes Turing-complete Bitcoin contracts verified by fraud proofs without consensus changes; development is under the ZeroSync nonprofit ([bitvm.org](https://bitvm.org/) (accessed 2026-11-24), [C-034](../docs/claims.md)).

**Open question:** Production maturity of Discrete Log Contracts for cap-table-related corporate actions in 2026 ([Q-002](../docs/claims.md)).

### Dependencies on chapters 01 to 04

- **Chapter 01:** Capital-table entries must reference a verifiable `entityId` and authorized signers from the signed portable entity record.
- **Chapter 02:** Every cap-table mutation needs an independently verifiable timestamp proof and a linked history digest.
- **Chapter 03:** Verifiers must validate asset-layer proofs, revocation status, and conflicting records without trusting a single operator.
- **Chapter 04:** Confidential cap-table details stay outside public anchors; only commitments or holder-presented selective disclosure may appear on public layers ([04-privacy-disclosure.md](04-privacy-disclosure.md)).

### What must be true before a normative chapter is justified

- At least one Bitcoin asset layer demonstrates production-grade security and auditability, and counsel can articulate how tokens might relate to share-register law under a named framework (**open question**, not a UCP legal claim).
- A portable entity record can bind asset-layer identifiers to authorized signers with revocation freshness guarantees ([03-verification.md](03-verification.md)).
- Interoperability or bridging between candidate layers (Taproot Assets, RGB, Arkade) is specified and tested for cap-table operations.

### Open questions for named kinds of experts

1. **Securities lawyers:** Which jurisdictional securities frameworks, if any, could recognize a Bitcoin-anchored token as part of a share register workflow without a traditional transfer agent ([Q-026](../docs/claims.md))?
2. **Bitcoin protocol engineers:** What Taproot Assets or RGB protocol changes would be required to support transfer restrictions, voting rights, and corporate actions natively?
3. **Corporate registrars:** What evidence would a registrar need to accept a cryptographically signed cap-table history as authoritative for its own records?

---

## 2. Universal Commercial Code (research topic, not US UCC)

### Problem

Commercial contracts across planetary boundaries lack a neutral, machine-readable framework for offer, acceptance, performance, and remedies that respects light-lag and differing supervisory states. Existing uniform codes are territorial and often assume near-instant communication.

### Existing standards or projects to evaluate first

**Verified fact (with source):** Outer Space Treaty Article VI requires state authorization and supervision of non-governmental space activities ([UNOOSA](https://www.unoosa.org/oosa/en/ourwork/spacelaw/treaties/outerspacetreaty.html) (accessed 2026-11-24), [C-002](../docs/claims.md)).

**Verified fact (with source):** As of 28 October 2026, NASA listed Vietnam as the 78th nation to sign the Artemis Accords ([NASA Artemis Accords](https://www.nasa.gov/artemis-accords/) (accessed 2026-11-24), [C-003](../docs/claims.md)).

**Verified fact (with source):** NASA describes the Artemis Accords as principles for civil space exploration reinforcing Outer Space Treaty commitments ([NASA Artemis Accords](https://www.nasa.gov/artemis-accords/) (accessed 2026-11-24), [C-004](../docs/claims.md)).

**Open question:** Whether UNCITRAL Model Law on Identity Management and Trust Services (2022) offers adaptable trust-service concepts; the UNCITRAL MLIT landing page returned HTTP 403 to automated fetch in this environment ([UNCITRAL MLIT](https://uncitral.un.org/en/mlit), [Q-008](../docs/claims.md), [Q-027](../docs/claims.md)).

**Assumption:** UNCITRAL arbitration and electronic commerce texts may provide comparators for cross-border recognition; individual texts were not machine-verified in this pass ([UNCITRAL arbitration](https://uncitral.un.org/en/texts/arbitration) (accessed 2026-11-24), [C-010](../docs/claims.md)).

**Verified fact (with source):** The U.S. Office of Space Commerce announced four SCC Pilot Phase participants on 12 November 2026 from nearly 40 applications ([OSC announcement](https://space.commerce.gov/osc-announces-the-space-commerce-certification-pilot-phase-cohort/) (accessed 2026-11-24), [C-038](../docs/claims.md)).

**Verified fact (with source):** EUobserver reported that the European Parliament ITRE committee adopted a weakened EU Space Act position on 19 November 2026, dropping the mandatory environmental certificate and moving space cybersecurity requirements toward NIS2 amendments ([EUobserver](https://euobserver.com/249952/meps-gut-eu-commission-plan-for-regulating-space-industries/) (accessed 2026-11-24), [C-039](../docs/claims.md)).

**Verified fact (with source):** NASA's Mars communications disruption paper describes multi-week direct Earth link blackout periods for representative crewed profiles ([NASA PDF](https://www.nasa.gov/wp-content/uploads/2024/01/mars-communications-disruption-and-delay.pdf) (accessed 2026-11-24), [C-026](../docs/claims.md)).

### Dependencies on chapters 01 to 04

- **Chapter 01:** Contract parties must be identifiable through verifiable entity records with authorized keys.
- **Chapter 02:** Contract formation timestamps and amendment history must be independently verifiable under light-lag.
- **Chapter 03:** Verification of contract execution evidence must not require real-time connectivity.
- **Chapter 04:** Confidential contract terms remain off public ledgers; only commitments or digests may be anchored ([04-privacy-disclosure.md](04-privacy-disclosure.md)).

### What must be true before a normative chapter is justified

- A delay-tolerant contract state machine is specified and demonstrated for round-trip times on the order of 6 to 44 minutes ([C-037](../docs/claims.md)).
- Supervisory-state authorization credentials can be attached to entity records and verified without a central registry (**proposal**; map to national pilots such as [C-038](../docs/claims.md) is exploratory only).
- Choice-of-law and dispute-resolution clauses reference existing arbitration rules rather than inventing a new court.

### Open questions for named kinds of experts

1. **Commercial lawyers:** Which UNCITRAL or similar model-law provisions can be adapted for machine-readable, delay-tolerant contract execution without new treaty negotiation ([Q-027](../docs/claims.md))?
2. **Space policy analysts:** How do current national mission-authorization regimes (for example the U.S. SCC pilot and the evolving EU Space Act) map to attachable credentials for a portable entity?
3. **Systems architects:** What data model supports contract state transitions that remain valid under Earth and Mars local time without a shared clock?

---

## 3. Interstellar Commercial Court (disputes)

### Problem

No neutral tribunal is established in UCP for commercial disputes between entities operating under different supervisory states with light-lag measured in minutes to hours. Existing arbitration rules often assume terrestrial connectivity and enforcement pathways.

### Existing standards or projects to evaluate first

**Verified fact (with source):** McGill's Institute of Air and Space Law hosts the Permanent Court of Arbitration Optional Rules for Arbitration of Disputes Relating to Outer Space Activities (PDF) ([McGill IASL space arbitration](https://www.mcgill.ca/iasl/research/space-law/space-arbitration) (accessed 2026-11-24), [C-040](../docs/claims.md)).

**Verified fact (with source):** Andrea Harrington and Vincent Correia are listed as Co-Directors of the McGill Institute of Air and Space Law ([McGill IASL about](https://www.mcgill.ca/iasl/about-us/about) (accessed 2026-11-24), [C-046](../docs/claims.md)).

**Open question:** Whether the Optional Rules have been used in a published commercial case in the 2020s ([Q-028](../docs/claims.md)).

**Verified fact (with source):** BitVM enables fraud-proof verification of Bitcoin contracts but is not a court or registrar ([bitvm.org](https://bitvm.org/) (accessed 2026-11-24), [C-034](../docs/claims.md)).

**Verified fact (with source):** Aon's Q1 2026 space insurance market report states that insurers remain extremely selective in underwriting launch and in-orbit risks ([Aon Q1 2026 report PDF](https://assets.aon.com/-/media/files/aon/capabilities/risk-transfer/space-insurance-market-report---q1-2026.pdf) (accessed 2026-11-24), [C-044](../docs/claims.md)).

**Assumption:** UNCITRAL arbitration texts remain relevant comparators for cross-border award enforcement ([C-010](../docs/claims.md)).

### Dependencies on chapters 01 to 04

- **Chapter 01:** Parties and authorized representatives must be verifiable from entity records.
- **Chapter 02:** Evidence submission timestamps and hearing schedules must accommodate light-lag.
- **Chapter 03:** Verification of cryptographic evidence (signatures, anchors, contract states) must be reproducible by arbitrators without vendor lock-in.
- **Chapter 04:** Confidential evidence must be disclosed to a tribunal without public exposure; selective disclosure and `evidence-withheld` semantics apply ([04-privacy-disclosure.md](04-privacy-disclosure.md), [Q-018](../docs/claims.md)).

### What must be true before a normative chapter is justified

- PCA Optional Rules or equivalent are confirmed as practically usable for commercial (not only state) disputes, with documented enforcement pathways (**open question** for counsel and arbitrators).
- A technical evidence package format lets arbitrators verify Bitcoin-anchored records, asset-layer states, and contract executions offline.
- Enforcement pathways for awards against off-world assets are understood and documented (**open question**).

### Open questions for named kinds of experts

1. **Arbitrators (PCA / McGill IASL):** Have the Optional Rules for outer space activities been used in a published commercial case, and what evidence formats would make a Bitcoin-anchored record useful to a tribunal ([Q-028](../docs/claims.md))?
2. **Bitcoin protocol engineers:** What BitVM or DLC constructions can express factual disputes (for example delivery or execution claims) without requiring the tribunal to run a full node?
3. **Insurers (space underwriters):** What identity, authorization, and incident evidence would make a new commercial space counterparty insurable, and how should dispute outcomes feed into underwriting ([C-044](../docs/claims.md))?

---

## 4. Universal Reputation Ledger

### Problem

Reputation signals for entities and agents need to be portable, verifiable, and resistant to sybil attacks without a central reputation authority. Many credential systems are jurisdiction-bound or lack governance for commercial trust at interplanetary scale.

### Existing standards or projects to evaluate first

**Verified fact (with source):** After obtaining an LEI, a legal entity may obtain a vLEI through a Qualified vLEI Issuer ([GLEIF Get a vLEI](https://www.gleif.org/en/organizational-identity/get-an-lei-vlei/get-a-vlei) (accessed 2026-11-24), [C-013](../docs/claims.md)).

**Verified fact (with source):** GLEIF publishes vLEI Ecosystem Governance Framework version 4.0 with Primary Document version 1.2 dated 25 March 2026 ([GLEIF vLEI EGF](https://www.gleif.org/en/organizational-identity/become-a-vlei-issuer-qvi/vlei-ecosystem-governance-framework) (accessed 2026-11-24), [C-041](../docs/claims.md)).

**Verified fact (with source):** The framework includes Technical Requirements Part 1: KERI Infrastructure version 1.4 dated 25 March 2026 ([GLEIF vLEI EGF](https://www.gleif.org/en/organizational-identity/become-a-vlei-issuer-qvi/vlei-ecosystem-governance-framework) (accessed 2026-11-24), [C-014](../docs/claims.md)).

**Verified fact (with source):** The KERI Foundation lists Samuel M. Smith as Technical Lead manager, Henk van Cann as Chairman, and Karla McKenna as Advisory Lead on its board ([KERI Foundation governance](https://keri.foundation/about/board-governance/) (accessed 2026-11-24), [C-042](../docs/claims.md)).

**Verified fact (with source):** W3C Verifiable Credentials 2.0 became a W3C Recommendation on 15 May 2025 ([W3C news](https://www.w3.org/news/2025/the-verifiable-credentials-2-0-family-of-specifications-is-now-a-w3c-recommendation/) (accessed 2026-11-24), [C-012](../docs/claims.md)).

**Verified fact (with source):** Proof announced the x401 agent authorization protocol on 15 October 2026 ([Proof blog](https://www.proof.com/blog/proof-launches-x401-giving-ai-agents-a-way-to-prove-who-they-represent---and-what-theyre-authorized-to-do) (accessed 2026-11-24), [C-023](../docs/claims.md)).

### Dependencies on chapters 01 to 04

- **Chapter 01:** Reputation credentials must bind to a verifiable `entityId` and authorized keys.
- **Chapter 02:** Reputation events (issuance, revocation, endorsement) require independently verifiable timestamps and history links.
- **Chapter 03:** Verifiers must validate credential chains and revocation status without trusting a single directory.
- **Chapter 04:** Sensitive reputation claims must support selective disclosure and remain off public anchors ([04-privacy-disclosure.md](04-privacy-disclosure.md), [C-029](../docs/claims.md)).

### What must be true before a normative chapter is justified

- A governance framework defines who may issue reputation credentials, under what policies, and how relying parties evaluate them, without implying a new global directory.
- vLEI interoperability is demonstrated: a portable entity record can present a vLEI credential as an attached claim without implying the record itself is a legal person ([Q-029](../docs/claims.md)).
- Sybil resistance for agent reputations is achieved through binding to human or institutional principals (for example delegated authorization models) rather than token staking alone.

### Open questions for named kinds of experts

1. **GLEIF / KERI standards leads:** How could a portable entity record bind to an LEI or vLEI without implying the cryptographic record is a legal person, and what would a verifier need to accept that binding ([Q-029](../docs/claims.md))?
2. **Commercial lawyers:** Which existing reputation or credit-reporting frameworks could recognize a verifiable credential as a permissible factor, and what remains **open question** for cross-border effect?
3. **AI-agent platform builders:** What revocation and delegation semantics are required for agent reputation credentials to remain valid across light-lag partitions ([C-023](../docs/claims.md))?

---

## 5. Interstellar Settlement Layer

### Problem

Final settlement of commercial obligations across planetary distances must tolerate minutes to hours of light-lag, conjunction blackouts lasting weeks, and no shared mempool. Lightning and L402 assume low-latency connectivity and are not presumed suitable for interplanetary settlement ([Q-003](../docs/claims.md)).

### Existing standards or projects to evaluate first

**Verified fact (with source):** The IETF Delay/Disruption Tolerant Networking Working Group is Active; its charter states Bundle Protocol v7 and related specifications are published and used in production by governments and commercial organizations worldwide ([IETF DTN WG](https://datatracker.ietf.org/wg/dtn/about/) (accessed 2026-11-24), [C-036](../docs/claims.md)).

**Verified fact (with source):** Bundle Protocol version 7 is [RFC 9171](https://www.rfc-editor.org/rfc/rfc9171.html) (accessed 2026-11-24), [C-021](../docs/claims.md)).

**Verified fact (with source):** NASA's Mars communications disruption paper describes inevitable multi-day to multi-week blackout periods for representative direct Earth links ([NASA PDF](https://www.nasa.gov/wp-content/uploads/2024/01/mars-communications-disruption-and-delay.pdf) (accessed 2026-11-24), [C-026](../docs/claims.md)).

**Verified fact (with source):** Unchained's Bitcoin Astronomy essay states Mars is 3 to 22 light-minutes away, round-trip 6 to 44 minutes, and cites a 10-minute Bitcoin block time ([Unchained](https://www.unchained.com/bitcoin-astronomy/the-law-of-hash-horizons) (accessed 2026-11-24), [C-037](../docs/claims.md)).

**Verified fact (with source):** Blockstream Satellite broadcasts the Bitcoin blockchain worldwide to Earth receivers ([Blockstream Satellite](https://blockstream.github.io/satellite/) (accessed 2026-11-24), [C-025](../docs/claims.md)).

**Verified fact (with source):** Lightning Labs describes L402 as Lightning machine payment authentication for API access ([Lightning Engineering](https://lightning.engineering/posts/2026-02-11-ln-agent-tools/) (accessed 2026-11-24), [C-022](../docs/claims.md)).

**Verified fact (with source):** PyPI lists `opentimestamps-client` version 0.8.0 published 27 October 2026 ([PyPI](https://pypi.org/project/opentimestamps-client/) (accessed 2026-11-24), [C-020](../docs/claims.md)).

### Dependencies on chapters 01 to 04

- **Chapter 01:** Settlement instructions must reference verifiable entity identifiers and authorized signers.
- **Chapter 02:** Settlement proofs require independently verifiable timestamps that remain valid after calendar failure ([Q-010](../docs/claims.md)).
- **Chapter 03:** Verifiers must confirm settlement finality under stated confirmation assumptions without real-time node access ([Q-009](../docs/claims.md)).
- **Chapter 04:** Settlement amounts and counterparties may be confidential; only commitments or zero-knowledge proofs may appear on public layers ([04-privacy-disclosure.md](04-privacy-disclosure.md)).

### What must be true before a normative chapter is justified

- A delay-tolerant settlement protocol uses BPv7 or equivalent for message transport and defines timeout, retry, and finality rules for 6 to 44 minute round trips ([C-037](../docs/claims.md), [Q-011](../docs/claims.md)).
- Bitcoin anchoring is treated as delayed proof, not real-time finality; local settlement layers operate per planet with periodic cross-planet reconciliation (**proposal**).
- Agent spend limits (L402 macaroons) are expressed in terms of local settlement finality, not Earth mempool confirmation alone ([C-022](../docs/claims.md)).

### Open questions for named kinds of experts

1. **DTN WG chairs (Edward J. Birrane, Rick Taylor):** What DTN assumptions should a commercial settlement protocol reuse, and where do payment protocols need a different model than store-and-forward bundles ([Q-030](../docs/claims.md))?
2. **Bitcoin protocol engineers:** Which local settlement constructions (Lightning, Arkade, DLCs, RGB) can operate with minutes-to-hours of partition and still provide cryptographic proof of finality after reconnection?
3. **Space operators:** What data-availability and delay profiles should a delay-tolerant Bitcoin client assume, and what does current satellite broadcast not solve for interplanetary settlement ([C-025](../docs/claims.md))?

---

## 6. Algorithmic Governance Framework

### Problem

Automated decision-making for entities and agents (treasury limits, parameter changes, emergency pauses) must be auditable, revocable, and binding on authorized signers without granting legal personality to code. Many DAO frameworks are jurisdiction-bound and assume synchronous voting.

### Existing standards or projects to evaluate first

**Verified fact (with source):** The Utah Division of Corporations publishes registration, renewal, and amendment processes for Limited Liability Decentralized Autonomous Organizations and encourages consulting an attorney ([Utah DAO](https://commerce.utah.gov/corporations/business-entities/dao/) (accessed 2026-11-24), [C-043](../docs/claims.md)).

**Open question:** How jurisdiction-specific DAO LLC programs record on-chain or off-chain governance relative to filed certificates; underlying statutes for non-U.S. programs were not machine-verified from primary parliamentary sources in this pass ([Q-031](../docs/claims.md)).

**Verified fact (with source):** Lightning Labs describes L402 scoped macaroons and remote signers for agent API access ([Lightning Engineering](https://lightning.engineering/posts/2026-02-11-ln-agent-tools/) (accessed 2026-11-24), [C-022](../docs/claims.md)).

**Verified fact (with source):** Proof announced x401 on 15 October 2026 for human-signed agent authorization terms ([Proof blog](https://www.proof.com/blog/proof-launches-x401-giving-ai-agents-a-way-to-prove-who-they-represent---and-what-theyre-authorized-to-do) (accessed 2026-11-24), [C-023](../docs/claims.md)).

**Verified fact (with source):** Repository article [001-the-missing-layer.md](../content/articles/001-the-missing-layer.md) states that granting AI systems legal personality is not proposed as a prerequisite and emphasizes bounded, revocable delegation ([C-045](../docs/claims.md)).

### Dependencies on chapters 01 to 04

- **Chapter 01:** Governance policies (thresholds, roles, emergency authorities) are recorded in the entity record and signed by authorized keys.
- **Chapter 02:** Policy changes and automated action logs require independently verifiable timestamps and history links.
- **Chapter 03:** Verifiers must confirm that an automated action complied with the policy in force at the effective time, including key validity and revocation status.
- **Chapter 04:** Governance parameters may be confidential; only policy commitments or compliance proofs may be public ([04-privacy-disclosure.md](04-privacy-disclosure.md)).

### What must be true before a normative chapter is justified

- A policy language expresses spending limits, role-based authorities, and emergency procedures in machine-executable form with verifiable compliance properties (**proposal**).
- At least one jurisdictional filing practice demonstrates how algorithmic governance rules map to a recognized legal entity wrapper without UCP claiming recognition ([Q-031](../docs/claims.md)).
- Agent authorization credentials integrate with governance policies so automated acts are traceable to a human or institutional principal ([C-023](../docs/claims.md)).

### Open questions for named kinds of experts

1. **DAO legal wrapper practitioners:** How does a filed DAO LLC record authorized human or agent signers today, and what would a portable, independently verifiable history add ([Q-031](../docs/claims.md))?
2. **Formal methods / smart contract auditors:** What policy language or DSL supports treasury limits, role delegation, and emergency pauses with proofs of compliance that are verifiable years later?
3. **AI-agent platform builders:** Which authorization fields must be signed by the principal, and how is revocation expected to work across agents, websites, and planetary partitions ([C-023](../docs/claims.md), [Q-004](../docs/claims.md))?

---

## Readiness summary

| Topic | Readiness | First question to answer |
| --- | --- | --- |
| Universal Capital Table | research only | Which Bitcoin asset layer, if any, can satisfy a recognized securities framework for a share register without a traditional transfer agent ([Q-026](../docs/claims.md))? |
| Universal Commercial Code | research only | Which UNCITRAL or model-law provisions can be adapted for machine-readable, delay-tolerant contract execution without new treaty negotiation ([Q-027](../docs/claims.md))? |
| Interstellar Commercial Court (disputes) | research only | Have the PCA Optional Rules for outer space activities been used in a published commercial case, and what evidence formats would make a Bitcoin-anchored record useful to a tribunal ([Q-028](../docs/claims.md))? |
| Universal Reputation Ledger | research only | How could a portable entity record bind to an LEI or vLEI without implying the cryptographic record is a legal person ([Q-029](../docs/claims.md))? |
| Interstellar Settlement Layer | research only | What DTN assumptions should a commercial settlement protocol reuse, and where do payment protocols need a different model than store-and-forward bundles ([Q-030](../docs/claims.md))? |
| Algorithmic Governance Framework | research only | How does a filed DAO LLC record authorized human or agent signers today, and what would a portable, independently verifiable history add ([Q-031](../docs/claims.md))? |

## Chapter open questions

1. **Governance (repository):** What single canonical naming scheme should replace the split between website UCP-* layer names and repository acronyms, given URL and UCC-X collisions noted in [README.md](README.md#open-questions)?
2. **Cross-topic:** Which of the six topics, if any, should graduate to numbered normative chapters before others, given dependencies on [Q-005](../docs/claims.md) serialization and [Q-009](../docs/claims.md) anchor confirmation depth?
3. **Law (external experts):** For each topic, which claims in this index require counsel review before any implementation pilot references them externally?