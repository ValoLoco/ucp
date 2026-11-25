"""RFC 8785 (JCS) canonical JSON, restricted profile.

Proposal for this reference only: chapter 01 leaves the canonical
serialization open (Q-005). This module implements RFC 8785 for the value
types that chapter 01 records use: objects, arrays, strings, integers,
booleans and null. Non-integer numbers are rejected rather than formatted,
because RFC 8785 number formatting (ECMAScript rules) is not needed by any
chapter 01 field and is a common source of cross-implementation drift.
"""

from __future__ import annotations

import json

MAX_SAFE_INTEGER = 2**53 - 1


class CanonicalizationError(ValueError):
    pass


def _utf16_key(s: str) -> list[int]:
    # RFC 8785 section 3.2.3: sort member names by UTF-16 code units.
    data = s.encode("utf-16-be")
    return [int.from_bytes(data[i : i + 2], "big") for i in range(0, len(data), 2)]


def _ser(value, out: list[str]) -> None:
    if value is None:
        out.append("null")
    elif value is True:
        out.append("true")
    elif value is False:
        out.append("false")
    elif isinstance(value, int):
        if abs(value) > MAX_SAFE_INTEGER:
            raise CanonicalizationError("integer outside IEEE 754 safe range")
        out.append(str(value))
    elif isinstance(value, float):
        raise CanonicalizationError("non-integer numbers are not allowed in this profile")
    elif isinstance(value, str):
        # json.dumps with ensure_ascii=False matches RFC 8785 string escaping
        # (short escapes for \b \f \n \r \t, \u00XX for other controls,
        # everything else literal UTF-8).
        out.append(json.dumps(value, ensure_ascii=False))
    elif isinstance(value, list):
        out.append("[")
        for i, item in enumerate(value):
            if i:
                out.append(",")
            _ser(item, out)
        out.append("]")
    elif isinstance(value, dict):
        for k in value:
            if not isinstance(k, str):
                raise CanonicalizationError("object keys must be strings")
        out.append("{")
        for i, k in enumerate(sorted(value, key=_utf16_key)):
            if i:
                out.append(",")
            out.append(json.dumps(k, ensure_ascii=False))
            out.append(":")
            _ser(value[k], out)
        out.append("}")
    else:
        raise CanonicalizationError(f"unsupported type: {type(value).__name__}")


def canonicalize(value) -> bytes:
    out: list[str] = []
    _ser(value, out)
    return "".join(out).encode("utf-8")
