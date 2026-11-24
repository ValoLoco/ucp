# Specification chapters

Normative text will be drafted **one chapter per pull request** (see [../CONTRIBUTING.md](../CONTRIBUTING.md)). Use [\_template.md](_template.md) for new chapters.

## Chapter map

| Chapter | Title | Status |
| --- | --- | --- |
| [00](00-conventions.md) | Conventions and terminology (RFC 2119 keywords) | discussion draft |
| [01](01-entity-record.md) | Signed portable entity record | discussion draft |
| [02](02-entity-history.md) | History and timestamping | discussion draft |
| 03 | Verification | not started |
| 04 | Privacy and disclosure | not started |
| 05 | Later-layer research topics (cap table, contracts, disputes, reputation, settlement, governance) | not started |

## Existing drafts (outside numbered chapters)

| Document | Status |
| --- | --- |
| [core-v0.1.md](core-v0.1.md) | concept draft |

Chapter [01](01-entity-record.md) supersedes `core-v0.1.md` for normative field and verification text; `core-v0.1.md` remains as a historical concept draft.

## Chapter 05 scope (research only)

Chapter 05 is an index of **research topics**, not normative requirements: Universal Capital Table, Universal Commercial Code, Interstellar Commercial Court, Universal Reputation Ledger, Interstellar Settlement Layer, and Algorithmic Governance Framework. Each topic needs its own requirements, legal review, and future chapters or specs if justified.

## Chapter template

Each normative chapter should follow the same sections as contribution proposals ([../CONTRIBUTING.md](../CONTRIBUTING.md)):

1. **Problem**
2. **Existing alternatives**
3. **Proposal**
4. **Trust assumptions**
5. **Legal implications**
6. **Privacy impact**
7. **Verification method**
8. **Smallest useful test**
9. **Open questions**

Copy [\_template.md](_template.md) when opening a chapter pull request.

## Open questions

- **Open:** settle one canonical layer naming scheme (website UCP-* vs repo acronyms); note URL collides with web URLs and UCC-X with the US Uniform Commercial Code.