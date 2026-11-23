# Decision 0001: Research before infrastructure

Status: proposed baseline for review.

## Context

The original seven-layer architecture combined legal ambitions with technology selections before validating their necessity or feasibility.

## Direction

**Assumption:** Use Bitcoin-first as a design direction. Start with a portable, signed entity record. Keep identity, legal recognition, contract interpretation, payment execution, and dispute enforcement distinct. Select dependencies only after comparing existing standards and documenting trust assumptions in [docs/claims.md](../claims.md).

**Verified fact (with source):** `did:ion` is not a default DID recommendation; Microsoft Entra Verified ID ended `did:ion` preview support in December 2023 ([FAQ](https://learn.microsoft.com/en-us/entra/verified-id/verifiable-credentials-faq) (accessed 2026-11-23)).

## Consequences

No mandatory Stacks dependency, tokenized cap table, protocol token, or on-chain arbitration in the initial demonstrator. Later layers remain research topics (**proposal**). This reduces scope while preserving the broader vision.