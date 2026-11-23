# Chapter 00: Conventions and terminology

Status: discussion draft. Not an interoperability standard or production implementation.

## Problem

Readers and implementers need shared rules for reading UCP specification chapters: how requirement strength is expressed, how draft maturity and evidence are labeled, how examples differ from requirements, how versions are named, and which serialization and time formats remain undecided. Without chapter 00, later chapters risk inconsistent keywords, ambiguous normative text, and untestable claims.

## Existing alternatives

Many IETF and W3C specifications adopt [BCP 14](https://www.rfc-editor.org/info/bcp14) requirement keywords defined in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and clarified in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174). Timestamps in Internet protocols commonly use the date-time format defined in [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339). Software releases often follow [Semantic Versioning 2.0.0](https://semver.org/). JSON interchange sometimes specifies canonical forms such as [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) (JSON Canonicalization Scheme, JCS). Binary alternatives include [RFC 8949](https://www.rfc-editor.org/rfc/rfc8949) (CBOR), which defines deterministic encoding rules in its Section 4.2.

UCP defers choosing a single on-wire serialization; [core-v0.1.md](core-v0.1.md) lists canonical serialization among decisions still required.

## Proposal

### Requirement keywords (BCP 14)

**Verified fact:** [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174) define interoperable meanings for requirement keywords in English prose.

**Proposal:** UCP normative chapters MUST use only the following keywords in requirement sentences, with meanings per [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) as updated by [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174): **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL**. Requirement keywords appear in uppercase in normative sentences. Lowercase uses of these words are informative unless explicitly marked otherwise.

Imperatives outside that set (for example "need to" or "is expected to") SHOULD NOT appear in normative requirements; rephrase to BCP 14 keywords or move text to informative sections.

### Document status labels

**Proposal:** Each specification chapter and standalone spec file carries exactly one document status label:

| Label | Meaning |
| --- | --- |
| concept draft | Early shape; may contradict other drafts; not suitable for implementation claims |
| discussion draft | Published for review; structure stabilizing; breaking edits expected |
| candidate | Intended complete for one protocol version; only editorial or bugfix changes expected before stable |
| stable | Identified with a released protocol version; breaking changes require a new major version |
| superseded | Replaced by a named successor chapter or version; retained for history |

Repository chapter map statuses are documented in [README.md](README.md). This chapter 00 is **discussion draft**.

### Claim and evidence labels

**Verified fact:** [docs/research/assumptions-and-corrections.md](../docs/research/assumptions-and-corrections.md) requires tracking statements as verified fact, proposal, assumption, or open question, with a primary source for external claims.

**Proposal:** In UCP specs and normative tables, authors label non-keyword assertions as one of:

| Label | Use |
| --- | --- |
| verified fact (with source) | Externally checkable; cite primary source URL or in-repo primary reference |
| proposal | Design direction under review; may change without a version bump while in discussion draft |
| assumption | Dependency treated as true for reasoning; must be falsifiable or revisable |
| open question | Unsettled; listed in chapter Open questions or tracked in issues |

Legal or regulatory **effects** MUST NOT be labeled verified fact unless supported by cited primary legal text and qualified review; default to open question or assumption per [CONTRIBUTING.md](../CONTRIBUTING.md).

**Proposal:** New or updated verified facts with external sources SHOULD be recorded in [docs/claims.md](../docs/claims.md). Informative documents under `docs/`, `content/`, and the root README SHOULD use the same four claim labels; long-term vision and layer maps are **proposal**, not implementation commitments.

### Normative and informative text

**Proposal:**

- Sections introduced as normative specify requirements using BCP 14 keywords.
- Sections introduced as informative explain rationale, document status, mappings to other systems, or historical notes. Informative text does not create requirements unless it restates a normative requirement by explicit reference.
- **Examples** are informative. Mark them with a clear heading such as `### Example` or the prefix `Example:` on a block. Example record field values, entity names, jurisdictions, keys, and hashes MUST be fictional unless wrapped in a verified fact citation to a public test vector document.
- **Notes** (non-normative clarifications) SHOULD be prefixed with `Note:`.

### Protocol and chapter versioning

**Proposal:** Name released protocol editions with semantic versioning as described at [https://semver.org/](https://semver.org/):

- **MAJOR** increments for incompatible record or verification behavior.
- **MINOR** increments for backward-compatible additions.
- **PATCH** increments for backward-compatible corrections or clarifications.

Record field `protocolVersion` (see [core-v0.1.md](core-v0.1.md)) SHOULD identify the protocol edition an instance claims to follow once chapter 01 defines the binding.

**Proposal:** Numbered chapters use a two-digit id (this file: `00`) and a slug filename (`00-conventions.md`). Chapter text MAY cite "UCP chapter MM" independently of protocol semver until a mapping table is adopted in a future chapter.

### Identifiers and field naming

**Verified fact:** [core-v0.1.md](core-v0.1.md) lists minimum record fields in camelCase (for example `entityId`, `protocolVersion`, `previousRecordDigest`, `effectiveAt`).

**Proposal:** New record and message field names in normative chapters MUST use camelCase ASCII identifiers unless a cited external standard requires a different shape for embedded objects.

**Open question (unchanged):** Canonical names for the seven protocol layers remain unsettled. The website labels (UCP-*) and repository acronyms (ULEI, UCT, UCC-X, ICC-X, URL, ISL, AGF) differ; acronym **URL** collides with web URLs and **UCC-X** with the US Uniform Commercial Code. See [specs/README.md](README.md#open-questions). This chapter does not resolve layer naming.

### Time and dates

**Proposal:** Serialized timestamps in examples and future test vectors SHOULD use [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339) profile strings unless a later chapter defines a different on-wire type.

**Verified fact:** [core-v0.1.md](core-v0.1.md) defines `effectiveAt` as claimed effective time, not a trusted timestamp.

**Proposal:** Verifiers MUST NOT treat `effectiveAt` as proof of when a record was created, agreed, or filed with any authority. Trusted time, if needed, comes from separate evidence (for example anchor receipts under stated assumptions), not from the claim alone.

### Encoding and serialization (open)

**Verified fact:** [core-v0.1.md](core-v0.1.md) states that canonical serialization, digest algorithm, and signature suite must be selected and tested before interoperability claims.

**Open question:** UCP has not selected a mandatory on-wire encoding. Candidates for future comparison include:

| Candidate | Primary reference |
| --- | --- |
| JSON with JCS canonicalization for signing and digest inputs | [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) |
| CBOR with deterministic encoding | [RFC 8949](https://www.rfc-editor.org/rfc/rfc8949) Section 4.2 |

Chapter 01 or a dedicated serialization chapter MUST pick one canonical representation (and digest and signature bindings) before implementers may claim cross-vendor interoperability. Until then, examples MAY use human-readable JSON for readability only; such examples are not normative wire formats.

## Trust assumptions

- Readers understand English requirement keywords per [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).
- Reviewers apply document status labels honestly and do not treat discussion drafts as stable implementations.
- `effectiveAt` and similar fields reflect issuer claims; verifiers supply their own trust policy for time and authority.

## Legal implications

This chapter defines documentation and data conventions only. It does not claim legal recognition of entities, effect of signatures, validity of registrations, or enforceability of records in any jurisdiction. Legal questions belong in open questions or future chapters with qualified review.

## Privacy impact

Conventions do not mandate fields. Rules that examples use fictional data reduce accidental publication of real personal or confidential material in specs. Implementers remain responsible for keeping identity documents and confidential contracts off public records per [core-v0.1.md](core-v0.1.md).

## Verification method

1. Search the chapter for lowercase "must" or "should" in requirement contexts; confirm normative sections use BCP 14 uppercase keywords.
2. Confirm the chapter header status matches [README.md](README.md).
3. Confirm each external factual sentence links a primary source or is labeled proposal, assumption, or open question.
4. Confirm examples are marked and do not reuse live-looking identifiers without a citation to official test vectors.
5. Confirm no normative choice of JSON-JCS or CBOR appears outside the open encoding section.

## Smallest useful test

Apply this checklist to any specification chapter pull request:

1. **Status:** File header status label is present and matches the chapter map row in [specs/README.md](README.md).
2. **Template sections:** All nine sections from [_template.md](_template.md) exist (Problem through Open questions).
3. **BCP 14:** Normative requirements use RFC 2119 keywords in uppercase; no ambiguous imperatives in normative text.
4. **Claims:** External facts cite primary sources; other assertions are labeled proposal, assumption, or open question.
5. **Normative vs informative:** Examples and notes are marked; fictional data only in examples.
6. **Links:** Relative links resolve within the repository at the PR commit.
7. **Style:** No em dashes in new prose ([CONTRIBUTING.md](../CONTRIBUTING.md)).
8. **Scope:** No legal or regulatory conclusions stated as fact; unsettled law items are open questions.
9. **Encoding:** If wire format appears, it is either cited as open, explicitly proposed, or deferred to chapter 01.
10. **Open questions:** Section lists actionable questions for reviewers and external experts.

## Open questions

1. Should UCP adopt [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) JCS, [RFC 8949](https://www.rfc-editor.org/rfc/rfc8949) deterministic CBOR, or another canonicalization ruleset as the single mandatory serialization for signed entity records?
2. How should `protocolVersion` semver relate to individual chapter numbers when chapters land at different times (one global protocol version vs per-chapter revision ids)?
3. What single canonical naming scheme should replace the split between website UCP-* layer names and repository acronyms, given URL and UCC-X collisions noted in [specs/README.md](README.md)?
4. Which signature suites and digest algorithms pair with the chosen canonical serialization to meet independent verification goals in milestone 2 ([docs/roadmap.md](../docs/roadmap.md))?
5. When an anchor receipt is present, what normative language should distinguish Bitcoin confirmation assumptions from `effectiveAt` claims without implying court or registrar acceptance?
6. Should informative articles under `content/` carry the same document status labels as `specs/` chapters, and how do superseded articles point to replacement specs?