"""NFL parser stub using Lark."""
from __future__ import annotations

import re
from lark import Lark

_GRAMMAR = "start: (_NL | /[^\n]*/ NEWLINE)*\n%import common.NEWLINE -> _NL"
_PARSER = Lark(_GRAMMAR, parser="lalr")

VERSION_RE = re.compile(r"^//\s*NFL v(?P<ver>[0-9]+\.[0-9]+)")


def parse_nfl(text: str) -> list:
    """Parse NFL text and return an AST list.

    The implementation currently validates the leading version comment
    and otherwise returns an empty list as a placeholder.
    """
    lines = text.splitlines()
    if lines:
        m = VERSION_RE.match(lines[0].strip())
        if not m or m.group("ver") != "0.3":
            raise ValueError("NFL version mismatch")
    # Parse to verify syntax (stub grammar)
    _PARSER.parse(text)
    return []
