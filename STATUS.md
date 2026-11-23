# Project status

UCP is an early-stage **proposal** developed publicly through BUENATURA. No participating jurisdictions, institutional endorsements, legal recognition, deployed protocol, or production readiness are claimed.

Read this document alongside [README.md](README.md) and [docs/architecture.md](docs/architecture.md). Those documents mix **proposal** and **assumption** with a small set of **verified fact (with source)** context. Where they conflict with this status or [docs/research/assumptions-and-corrections.md](docs/research/assumptions-and-corrections.md), treat the status and research notes as authoritative.

**Assumption:** Bitcoin-first is the research direction. Stacks, ION, Taproot Assets, RGB, Lightning, and BitVM are candidates to evaluate, not required dependencies. **Verified fact (with source):** Taproot Assets is alpha software per Lightning Labs ([get-tapd](https://docs.lightning.engineering/lightning-network-tools/taproot-assets/get-tapd) (accessed 2026-11-23)). **Verified fact (with source):** `did:ion` is not a recommended default; Microsoft Entra Verified ID ended `did:ion` preview support in December 2023 ([FAQ](https://learn.microsoft.com/en-us/entra/verified-id/verifiable-credentials-faq) (accessed 2026-11-23)).

The seven layers are a problem map (**proposal**), not seven products to build immediately.

The first milestone is a signed, portable entity record with independently verifiable history. It does not create a legal person or issue securities.

No protocol token is proposed. Funding, stewardship, and final licensing require explicit decisions before implementation or external contributions.

Factual claims are tracked in [docs/claims.md](docs/claims.md). Labeling rules: [specs/00-conventions.md](specs/00-conventions.md).