# UCP Architecture v0.1

## Problem

Corporate law is terrestrial and jurisdiction-bound. A company exists only through one state registry. As commerce extends into orbit and beyond, it needs portable identity, ownership, contracts, dispute resolution, reputation, settlement, and governance.

## Stack

```text
L7 Algorithmic Governance Framework
L6 Interstellar Settlement Layer
L5 Universal Reputation Ledger
L4 Interstellar Commercial Court
L3 Universal Commercial Code
L2 Universal Capital Table
L1 Universal Legal Entity Identifier

Bitcoin L1: consensus, timestamping, finality
```

## Layer Specifications

### L1: ULEI

- Identity method: `did:ion`.
- Credentials: W3C Verifiable Credentials for legal-entity and jurisdictional-registration claims.
- Registrar bridge: a Stacks contract maps a ULEI to its DID, jurisdictions, and credential roots.
- Bitcoin anchor: periodic Merkle roots of the credential registry are committed through `OP_RETURN` or Ordinals.

### L2: UCT

- Asset standard: Taproot Assets.
- Universe: one Taproot Assets universe per participating jurisdiction.
- Asset: a share class or other security token.
- Logic: Clarity contracts govern transfer, split, voting, dividends, and pre-emptive rights.
- Compliance: off-chain KYC and AML validators co-sign permitted transfers.

### L3: UCC-X

- Templates: SAFE, SPA, services agreement, offtake agreement, and joint venture agreement.
- Language: Clarity on Stacks.
- Design rule: decidable logic, no unbounded loops, fixed execution cost.
- Light-lag: contract conditions use block height and timestamps with a light-lag buffer.

### L4: ICC-X

- Evidence: Bitcoin-anchored transcripts and Merkle commitments.
- Arbitration: Clarity contracts manage panel selection, evidence submission, rulings, and appeal windows.
- Enforcement: registrar jurisdictions recognize and enforce rulings through UCT controls.
- Escalation: BitVM2 challenge-response for high-value disputes.

### L5: URL

- Attestations: KYC, audits, insurance, delivery performance, and dispute outcomes.
- Storage: IPFS or Arweave, with Merkle roots anchored to Bitcoin.
- Verification: DID resolution and Stacks read-only calls.

### L6: ISL

- Bitcoin: Lightning Network.
- Stablecoins: Taproot Assets on Lightning.
- Real-world assets: Taproot Assets and Lightning swaps.
- Cross-asset: Boltz, Lightning Loop, and Taproot Assets exchange infrastructure.
- Time tolerance: HTLC timelocks parameterized by block height and light-lag safety factors.

### L7: AGF

- Proposals, voting, timelocks, and treasury controls in Clarity.
- Fiduciary invariants encoded as assertions.
- AI agents receive scoped, revocable authority through capability credentials.

## Roadmap

1. Protocol definition and reference implementations.
2. Orbital MVP: ULEI, UCT, UCC-X, ICC-X, URL, ISL, and AGF.
3. Cis-lunar extension: light-lag contracts, resource title registry, and parametric insurance.
4. Interplanetary extension: relativistic timelocks, Martian incorporation, and interplanetary identity infrastructure.

## Open Questions

- Which registrar jurisdictions should participate first?
- Should UCT v1 use Taproot Assets or RGB?
- Should ICC-X start with Clarity and migrate high-value disputes to BitVM2?
- Should AI-agent legal personality be included in v1 or deferred?
- How should UCP be funded without a protocol token?
