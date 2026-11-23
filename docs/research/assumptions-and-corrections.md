# Assumptions and corrections

Label key statements using [specs/00-conventions.md](../../specs/00-conventions.md). Cited facts are registered in [docs/claims.md](../claims.md).

## Legal boundaries

**Verified fact (with source):** The Outer Space Treaty requires state authorization and supervision of non-governmental space activities (Article VI) ([UNOOSA](https://www.unoosa.org/oosa/en/ourwork/spacelaw/treaties/outerspacetreaty.html) (accessed 2026-11-23)).

The absence of a universal incorporation regime does not imply a legal vacuum. Existing corporate law, contractual choice of law, arbitration, regulation, and international space law must be examined before proposing replacements.

A cryptographic identifier does not confer legal personality. A token does not automatically constitute a legally effective share register. A credential proves an issuer made a claim, not that a court accepts it.

**Proposal:** Recognition by states, registrars, courts, and regulators is a research path discussed in this project. No agreements exist within this repository. Safety zones under the Artemis Accords framework must not be described as automatically creating property rights without qualified space-law analysis ([NASA Artemis Accords](https://www.nasa.gov/artemis-accords/) (accessed 2026-11-23)).

Code can implement explicit rules but cannot exhaust fiduciary duties, interpret every contract, or replace due process. Arbitration enforcement is jurisdiction-dependent and must be assessed by qualified counsel ([UNCITRAL arbitration texts](https://uncitral.un.org/en/texts/arbitration) (accessed 2026-11-23)).

## Technical boundaries

Bitcoin confirmation confidence is not absolute finality. Anchoring establishes a commitment under stated verification assumptions, not the truth, legality, authorship, or availability of its contents.

Stacks and other adjacent networks introduce their own assumptions. They must not be presented as equivalent to direct Bitcoin execution. BitVM verification is not a court for deciding real-world disputes.

**Verified fact (with source):** Taproot Assets is alpha software ([Lightning Labs get-tapd](https://docs.lightning.engineering/lightning-network-tools/taproot-assets/get-tapd) (accessed 2026-11-23)). A Taproot Assets universe is not a legal jurisdiction. Securities restrictions and cross-network controls need an explicit, tested design. Stablecoin availability and issuer support must be checked rather than assumed.

**Verified fact (with source):** Bitcoin's proof-of-work difficulty targets an average of one block about every ten minutes ([Bitcoin whitepaper](https://bitcoin.org/bitcoin.pdf) (accessed 2026-11-23)). That interval alone does not establish interplanetary suitability.

**Verified fact (with source):** One-way Earth-Mars light time ranges from about 3 to about 22.4 minutes ([NASA Mars Relay Network](https://science.nasa.gov/mars/mars-relay-network/) (accessed 2026-11-23)). Communication delay, network partitions, mining distribution, reorganizations, data availability, channel monitoring, and dispute windows need separate analysis. Lightning is not presumed suitable for Earth-Mars settlement.

**Proposal:** Commercial "Starlink-style" Mars relay constellations for general commerce are not documented as existing operational services in NASA's Mars relay materials; treat such ideas as proposals, not deployed infrastructure.

## Identity note

**Verified fact (with source):** Microsoft Entra Verified ID supported `did:ion` in preview until December 2023; documentation describes migration to `did:web` ([Microsoft FAQ](https://learn.microsoft.com/en-us/entra/verified-id/verifiable-credentials-faq) (accessed 2026-11-23)). UCP does not treat `did:ion` as a default DID method.

## Evidence process

For every external claim, record a primary source, access date, relevant passage, limitations, and reviewer. Track statements using the labels in [specs/00-conventions.md](../../specs/00-conventions.md). Public articles must distinguish these categories.

Starting points for review:

- UNOOSA treaties: https://www.unoosa.org/oosa/en/ourwork/spacelaw/treaties.html
- UNCITRAL arbitration: https://uncitral.un.org/en/texts/arbitration
- GLEIF existing entity identifiers: https://www.gleif.org/
- W3C credentials: https://www.w3.org/TR/vc-data-model-2.0/
- OpenTimestamps: https://opentimestamps.org/
- Bitcoin developer documentation: https://developer.bitcoin.org/
- Claims register: [docs/claims.md](../claims.md)