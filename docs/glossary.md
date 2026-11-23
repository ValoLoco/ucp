# Glossary

Alphabetical terms already used in this repository. **Status** is either **proposal** (design direction under research) or **open question** (unsettled or needs primary-source work). External standards link to URLs from [assumptions-and-corrections.md](research/assumptions-and-corrections.md) or, where noted, an official site. If no primary source is linked in-repo yet, entries say **Open: source needed**.

## AGF (Algorithmic Governance Framework)

**Status: proposal.** L7 in the seven-layer map: entity governance, authority delegation, and AI-agent permissions (README.md, `docs/architecture.md`). Not in scope for the first milestone (STATUS.md, decision 0001).

## Anchor / anchoring

**Status: proposal.** Optional external commitment proof for a record (`specs/core-v0.1.md`, `anchorReceipt`). Bitcoin anchoring is described as establishing a commitment under stated verification assumptions, not truth or legality (`docs/research/assumptions-and-corrections.md`).

## Arweave

**Status: open question.** Mentioned as possible attestation storage alongside IPFS (`docs/architecture.md`). **Open: source needed** for a cited primary source in this repo.

## Attestation

**Status: proposal.** A verifiable claim or credential about an entity or performance (e.g. KYC, audits, dispute outcomes in layer URL sketches, `docs/architecture.md`). Presence of a credential does not prove court acceptance (`docs/research/assumptions-and-corrections.md`).

## Authorized keys

**Status: proposal.** Public keys, roles, validity periods, and revocation references in the minimum entity record (`specs/core-v0.1.md`).

## Authority policy

**Status: proposal.** Rules for who may authorize updates and how recovery works (`specs/core-v0.1.md`).

## Bitcoin

**Status: proposal (research direction).** Stated neutral base for timestamping, settlement finality, and anchoring in README.md and architecture; confirmation confidence is not absolute finality (`docs/research/assumptions-and-corrections.md`). Primary starting reference: [Bitcoin developer documentation](https://developer.bitcoin.org/).

## BitVM

**Status: open question.** Referenced for high-value dispute escalation in architecture sketches (`docs/architecture.md`). Listed as a candidate to evaluate, not a dependency (STATUS.md). **Open: source needed** in assumptions register.

## BUENATURA

**Status: proposal.** Public development and live-stream venue named in README.md and STATUS.md (not a protocol layer).

## Clarity

**Status: open question.** Smart-contract language named in architecture for Stacks-related designs (`docs/architecture.md`). **Open: source needed** in assumptions register.

## Entity record (portable entity record)

**Status: proposal.** Signed, portable record of claims, authority, and history; first milestone (`STATUS.md`, `specs/core-v0.1.md`). Does not imply legal recognition (`specs/core-v0.1.md`).

## Entity ID (`entityId`)

**Status: proposal.** Protocol identifier distinct from official registration numbers (`specs/core-v0.1.md`).

## GLEIF / LEI (Legal Entity Identifier)

**Status: open question.** Existing entity identifier ecosystem to compare against ULEI research. Starting review link: [GLEIF](https://www.gleif.org/) (`docs/research/assumptions-and-corrections.md`).

## HTLC (hashed timelock contract)

**Status: proposal.** Referenced for light-lag-tolerant settlement timelocks in ISL sketches (`docs/architecture.md`). Suitability for interplanetary use is an open question (`docs/research/assumptions-and-corrections.md`).

## ICC-X (Interstellar Commercial Court)

**Status: proposal (research only).** L4 dispute resolution and enforceable rulings in the layer map (README.md). Deferred from initial demonstrator (decision 0001). Arbitration enforcement is jurisdiction-dependent (`docs/research/assumptions-and-corrections.md`). UNCITRAL arbitration texts: [UNCITRAL](https://uncitral.un.org/en/texts/arbitration).

## ION (`did:ion`)

**Status: open question.** Identity method named in ULEI sketch (`docs/architecture.md`). Candidate to evaluate (STATUS.md). **Open: source needed** in assumptions register.

## IPFS

**Status: open question.** Possible off-chain storage for URL attestations (`docs/architecture.md`). **Open: source needed** in assumptions register.

## ISL (Interstellar Settlement Layer)

**Status: proposal (research only).** L6 multi-asset settlement with light-lag tolerance (README.md). Lightning named in architecture; Earth-Mars suitability not presumed (`docs/research/assumptions-and-corrections.md`).

## Legal registrations

**Status: proposal.** Claimed jurisdictions, official identifiers, and evidence references in the minimum record (`specs/core-v0.1.md`). Do not confer legal personality by themselves (`docs/research/assumptions-and-corrections.md`).

## Light lag / light-lag

**Status: open question.** Communication delay affecting contracts and settlement timing (`docs/architecture.md`, assumptions on interplanetary suitability). Requires separate analysis (`docs/research/assumptions-and-corrections.md`).

## Lightning Network

**Status: open question.** Named for ISL settlement (`docs/architecture.md`). Candidate to evaluate (STATUS.md). Official site not yet listed in assumptions register: **Open: source needed** (consider [lightning.network](https://lightning.network/) for future citation).

## Merkle root / Merkle commitment

**Status: proposal.** Commitment pattern for registries and evidence in architecture (`docs/architecture.md`).

## OpenTimestamps

**Status: open question.** Timestamping approach to evaluate for history and anchoring. Starting link: [OpenTimestamps](https://opentimestamps.org/) (`docs/research/assumptions-and-corrections.md`).

## Ordinals

**Status: open question.** Named as a possible Bitcoin anchor carrier in ULEI sketch (`docs/architecture.md`). **Open: source needed** in assumptions register.

## OP_RETURN

**Status: open question.** Named Bitcoin output type for anchor commits (`docs/architecture.md`). See [Bitcoin developer documentation](https://developer.bitcoin.org/) as a starting point.

## Previous record digest

**Status: proposal.** Link to the preceding accepted record in the chain of updates (`specs/core-v0.1.md`).

## Protocol token

**Status: open question.** Explicitly not proposed (STATUS.md). Funding without a token is an open question (`docs/architecture.md`).

## RGB

**Status: open question.** Alternative asset layer mentioned for UCT (`docs/architecture.md`, STATUS.md). **Open: source needed** in assumptions register.

## Settlement

**Status: proposal (research only).** Transfer and finality of value across assets and distances (layer ISL, README.md). Distinct from legal enforcement (decision 0001).

## Stacks

**Status: open question.** Adjacent network in architecture sketches (registrar bridge, Clarity). Candidate, not required (STATUS.md, decision 0001). Own trust assumptions (`docs/research/assumptions-and-corrections.md`). **Open: source needed** in assumptions register.

## Taproot Assets

**Status: open question.** Asset standard named for UCT and ISL (`docs/architecture.md`, STATUS.md). A Taproot Assets universe is not a legal jurisdiction (`docs/research/assumptions-and-corrections.md`). **Open: source needed** in assumptions register.

## UCC-X (Universal Commercial Code extension)

**Status: proposal (research only).** L3 standard commercial contracts and execution logic (README.md). Not in first milestone.

## UCT (Universal Capital Table)

**Status: proposal (research only).** L2 portable ownership and securities records (README.md). Token does not automatically constitute a legally effective share register (`docs/research/assumptions-and-corrections.md`). Taproot Assets vs RGB: **open question** (`docs/architecture.md`).

## UCP (Universal Company Protocol)

**Status: proposal.** Open research effort for portable company records and related layers (README.md, STATUS.md).

## ULEI (Universal Legal Entity Identifier)

**Status: proposal.** L1 portable, verifiable company identity (README.md). Compare with existing identifiers such as GLEIF LEI (`docs/research/assumptions-and-corrections.md`). Cryptographic identifier does not confer legal personality (`docs/research/assumptions-and-corrections.md`).

## UNCITRAL

**Status: open question.** Framework for examining arbitration assumptions. Starting link: [UNCITRAL arbitration texts](https://uncitral.un.org/en/texts/arbitration) (`docs/research/assumptions-and-corrections.md`).

## UNOOSA / space treaties

**Status: open question.** International space law context for research. Starting link: [UNOOSA treaties](https://www.unoosa.org/oosa/en/ourwork/spacelaw/treaties.html) (`docs/research/assumptions-and-corrections.md`).

## URL (Universal Reputation Ledger)

**Status: proposal (research only).** L5 verifiable attestations and operational history (README.md). Not the World Wide Web URL scheme.

## Verifiable Credentials (W3C VC)

**Status: open question.** Credential format cited in ULEI sketch (`docs/architecture.md`). Starting link: [W3C Verifiable Credentials Data Model](https://www.w3.org/TR/vc-data-model-2.0/) (`docs/research/assumptions-and-corrections.md`).

## W3C (credentials)

See **Verifiable Credentials** above.