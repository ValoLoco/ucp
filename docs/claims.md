# Claims and sources

Master register for **verified fact (with source)** statements used in UCP documents. Other labels appear inline only unless they encode a contested external fact. Verification date: 2026-11-23 unless noted.

| ID | Label | Claim (short) | Source | Where used |
| --- | --- | --- | --- | --- |
| C-001 | verified fact (with source) | Earth-Mars one-way light time ranges from about 3 minutes to about 22.4 minutes depending on orbital position. | [NASA Mars Relay Network](https://science.nasa.gov/mars/mars-relay-network/) | `docs/architecture.md`, `docs/research/assumptions-and-corrections.md` |
| C-002 | verified fact (with source) | Outer Space Treaty Article VI: states bear international responsibility for national space activities and must authorize and supervise non-governmental entities in outer space. | [UNOOSA Outer Space Treaty](https://www.unoosa.org/oosa/en/ourwork/spacelaw/treaties/outerspacetreaty.html) | `docs/architecture.md`, `docs/research/assumptions-and-corrections.md` |
| C-003 | verified fact (with source) | As of 2026-10-28, Vietnam became the 78th nation to sign the Artemis Accords (NASA). | [NASA Artemis Accords](https://www.nasa.gov/artemis-accords/) | `docs/architecture.md` |
| C-004 | verified fact (with source) | Artemis Accords reinforce commitments under the Outer Space Treaty and related agreements; they are a set of principles for civil space exploration. | [NASA Artemis Accords](https://www.nasa.gov/artemis-accords/) | `docs/architecture.md` |
| C-005 | verified fact (with source) | Taproot Assets is alpha software; Lightning Labs warns to use mainnet at your own risk. | [Lightning Labs Get Started (tapd)](https://docs.lightning.engineering/lightning-network-tools/taproot-assets/get-tapd) | `docs/architecture.md`, `STATUS.md`, `docs/research/assumptions-and-corrections.md` |
| C-006 | verified fact (with source) | Microsoft Entra Verified ID supported `did:ion` in preview until December 2023; `did:ion` is no longer a selectable trust system (only `did:web`). | [Microsoft Entra Verified ID FAQ](https://learn.microsoft.com/en-us/entra/verified-id/verifiable-credentials-faq) | `docs/architecture.md`, `docs/decisions/0001-research-first.md` |
| C-007 | verified fact (with source) | Bitcoin proof-of-work targets an average of one block about every ten minutes (moving average). | [Bitcoin whitepaper (PDF)](https://bitcoin.org/bitcoin.pdf) | `docs/research/assumptions-and-corrections.md` |
| C-008 | verified fact (with source) | W3C Verifiable Credentials Data Model defines machine-readable credentials and verification concepts. | [W3C VC Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/) | `docs/architecture.md`, `docs/research/assumptions-and-corrections.md` |
| C-009 | verified fact (with source) | GLEIF operates the global Legal Entity Identifier system for identifying legal entities in participating jurisdictions. | [GLEIF](https://www.gleif.org/) | `docs/architecture.md` |
| C-010 | verified fact (with source) | UNCITRAL publishes widely used texts on international commercial arbitration. | [UNCITRAL arbitration texts](https://uncitral.un.org/en/texts/arbitration) | `docs/research/assumptions-and-corrections.md` |
| C-011 | verified fact (with source) | Repository hero image exists at `content/UCP-Article 1.png`. | This repository (path on disk) | `content/streams/season-01.md`, `README.md` |

## Proposals and assumptions tracked here (not facts)

| ID | Label | Claim (short) | Notes |
| --- | --- | --- | --- |
| P-001 | proposal | Starlink-style commercial Mars relay constellations for general commerce. | **Verified fact (with source):** NASA describes the Mars Relay Network (Odyssey, MRO, TGO, etc.), not a Starlink-class commercial service ([C-001 source](https://science.nasa.gov/mars/mars-relay-network/)). |
| P-002 | proposal | Seven-layer UCP stack (ULEI through AGF) as a problem map. | See `docs/architecture.md`; not a deployment plan. |
| P-003 | assumption | Bitcoin-first anchoring for optional commitments and settlement research. | See `docs/decisions/0001-research-first.md`. |
| P-004 | assumption | Stacks/Clarity, BitVM2, or Lightning for later layers if requirements justify them. | No production dependency claimed. |

## Open questions (no stable external source)

| ID | Label | Topic |
| --- | --- | --- |
| Q-001 | open question | Which registrar jurisdictions might participate in a future pilot. |
| Q-002 | open question | Whether Taproot Assets or RGB fits a future ownership-record experiment. |
| Q-003 | open question | Earth-Mars settlement patterns using Lightning or HTLCs under long light lag. |
| Q-004 | open question | Whether AI agents should receive legal personality in any UCP version. |

## Removed or softened in this audit

- **Removed:** None. Vision and architecture text was retained and relabelled.
- **Corrected:** `content/streams/season-01.md` previously said the hero image was not in the repository; it is present (**C-011**).

## Unresolved claims

No mandatory factual assertions remain without a label. Numeric signatory counts use NASA's dated statement only (**C-003**). State Department copy that lagged NASA on total signatories was not used as the canonical count.