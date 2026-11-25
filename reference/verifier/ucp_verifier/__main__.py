"""CLI: python -m ucp_verifier <fixture-or-input.json>

Input JSON: {"record": {...}, "predecessor": {...}?, "bundle": [...]?,
"policy": {...}?, "evidence": {...}?}. Prints the result object.
"""

import json
import sys

from .verify import verify_record


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        sys.stderr.write(__doc__)
        return 2
    with open(argv[1], encoding="utf-8") as fh:
        data = json.load(fh)
    result = verify_record(
        data.get("record"),
        predecessor=data.get("predecessor"),
        bundle=data.get("bundle", []),
        policy=data.get("policy"),
        evidence=data.get("evidence"),
    )
    print(json.dumps(result, indent=2))
    return {"valid": 0, "indeterminate": 3, "invalid": 1}[result["status"]]


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
