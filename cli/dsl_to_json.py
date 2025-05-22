"""Convert the pilot DSL into the JSON structure understood by the CLI."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any, Dict, List


def parse_file(path: str) -> Dict[str, Any]:
    """Parse *path* containing the simplified DSL and return a JSON graph."""
    pack = ""
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    with open(path, "r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("//"):
                continue

            if line.startswith("namespace"):
                parts = line.split()
                if len(parts) > 1:
                    pack = parts[1]
                continue

            if line.startswith("node "):
                m = re.match(r"node\s+(\w+)", line)
                if m:
                    # Initialize node with basic properties
                    node = {"name": m.group(1), "type": "record", "fields": []}
                    nodes.append(node)
                    # Here we would need additional logic to parse the node body
                    # by reading subsequent lines until the node block ends
                continue
            if line.startswith("edge ") and "->" in line:
                from_part: str
                to_part: str
                m = re.match(r"edge\s+\w+\s*:(.*?)->(.*)", line)
                if m:
                    from_part = m.group(1).strip()
                    to_part = m.group(2).strip()
                else:
                    m = re.match(r"edge\s+(\w+)\s*->\s*(\w+)", line)
                    if not m:
                        continue
                    from_part = m.group(1)
                    to_part = m.group(2)
                to_part = to_part.rstrip("{").strip().strip('"')
                edges.append({"from": from_part, "to": to_part})
                continue

    return {"pack": pack, "nodes": nodes, "edges": edges}


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert pilot DSL to NFL JSON")
    parser.add_argument("file", help="Path to DSL file")
    parser.add_argument("-o", "--out", metavar="FILE", help="Output JSON file")
    args = parser.parse_args(argv)

    graph = parse_file(args.file)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(graph, fh, indent=2)
    else:
        json.dump(graph, sys.stdout, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

__all__ = ["parse_file", "main"]
