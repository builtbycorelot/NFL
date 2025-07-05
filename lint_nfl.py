#!/usr/bin/env python3
"""Simple NFL linter for Node Form Language v2.0.0.

This script checks an NFL file for common formatting and syntax issues
including indentation, node and edge declarations, trait blocks and
duplicate node identifiers. It is intentionally minimal and does not
fully parse the language.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

NODE_RE = re.compile(r"^node:\s+(?P<id>\S+)$")
EDGE_RE = re.compile(r"^edge:\s+(\S+)\s+->\s+(\S+)\s+->\s+(\S+)$")
PROP_RE = re.compile(r"^\|\s+\w[\w.-]*:\s+.+$")
TRAIT_START_RE = re.compile(r"^\|\s+trait\.\w+$")


class NFLint:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.errors: list[str] = []
        self.nodes: set[str] = set()
        self.in_trait = False

    def lint(self) -> None:
        for lineno, raw in enumerate(self.path.read_text().splitlines(), 1):
            line = raw.rstrip()
            indent = len(line) - len(line.lstrip(" "))
            if "\t" in line:
                self.errors.append(f"{lineno}: tabs are not allowed")
            if indent % 2 != 0:
                self.errors.append(
                    f"{lineno}: indentation must be multiples of 2 spaces"
                )
            stripped = line.lstrip()
            if not stripped:
                continue
            if indent == 0:
                self._check_top_level(lineno, stripped)
            elif indent == 2:
                self._check_prop_or_trait(lineno, stripped)
            elif indent == 4:
                self._check_trait_prop(lineno, stripped)
            else:
                self.errors.append(f"{lineno}: unexpected indentation level")

    def _check_top_level(self, lineno: int, text: str) -> None:
        self.in_trait = False
        if text.startswith("pack:"):
            return
        if m := NODE_RE.match(text):
            node_id = m.group("id")
            if node_id in self.nodes:
                self.errors.append(f"{lineno}: duplicate node identifier '{node_id}'")
            else:
                self.nodes.add(node_id)
            return
        if EDGE_RE.match(text):
            return
        self.errors.append(f"{lineno}: unknown or invalid top-level line")

    def _check_prop_or_trait(self, lineno: int, text: str) -> None:
        if TRAIT_START_RE.match(text):
            self.in_trait = True
            return
        if PROP_RE.match(text):
            return
        self.errors.append(f"{lineno}: invalid property or trait declaration")

    def _check_trait_prop(self, lineno: int, text: str) -> None:
        if not self.in_trait:
            self.errors.append(f"{lineno}: trait property outside of trait block")
            return
        if PROP_RE.match(text):
            return
        self.errors.append(f"{lineno}: invalid trait property line")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: lint_nfl.py <file.nfl>")
        sys.exit(1)
    path = Path(sys.argv[1])
    linter = NFLint(path)
    linter.lint()
    if linter.errors:
        for msg in linter.errors:
            print(f"Error: {msg}")
        sys.exit(1)
    print("NFL lint passed")
