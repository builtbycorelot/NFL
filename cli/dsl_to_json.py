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
                # A more robust regex that can handle both formats described in the docs
                m = re.match(r"edge\s+(\w+)\s*(?::\s*)?([^-]*?)\s*->\s*([^{]*)", line)
                if not m:
                    continue

                from_node = m.group(1)
                from_field = m.group(2).strip() if m.group(2) else ""
                to_node = m.group(3).strip().strip('"')

                edge = {"from": from_node}
                if from_field:
                    edge["from_field"] = from_field
                edge["to"] = to_node

                edges.append(edge)
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
