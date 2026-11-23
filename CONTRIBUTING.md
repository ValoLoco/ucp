# Contributing

UCP welcomes precise objections, primary-source research, proposed specifications, and small reproducible experiments.

Read [STATUS.md](STATUS.md), [specs/00-conventions.md](specs/00-conventions.md), and [docs/research/assumptions-and-corrections.md](docs/research/assumptions-and-corrections.md) first. Add or update entries in [docs/claims.md](docs/claims.md) when introducing new **verified fact (with source)** statements.

## Documentation and specifications

- Doc index and reading order: [docs/README.md](docs/README.md)
- Spec chapter map: [specs/README.md](specs/README.md)
- New spec chapters: copy [specs/_template.md](specs/_template.md)

Normative specification work should land as **one spec chapter per pull request**, aligned with the chapter map in `specs/README.md`.

## Proposal format

Describe the problem, existing alternatives, proposed change, trust assumptions, legal implications, privacy impact, verification method, and smallest useful test. Clearly separate facts from proposals using the claim labels.

## Working principles

- Maximum strength, minimum weight.
- Build only what current requirements justify.
- Keep documents and code readable by humans and AI.
- Prefer open standards and independently verifiable claims.
- Do not claim endorsement or recognition without **verified fact (with source)** evidence.
- Never commit secrets, personal identity documents, or confidential contracts.
- Avoid em dashes and en dashes in project copy; use hyphens or rewrite.

## Review

Use issues for discussion and pull requests for changes. Record consequential decisions in `docs/decisions/`. No merge, informal poll, or live-stream discussion creates legal recognition.

## Licensing caution

The initial README proposes CC-BY-4.0 for specifications and MIT for code. Exact scope, copyright attribution, license texts, and contribution terms must be finalized before accepting external contributions. Do not assume third-party materials may be relicensed.