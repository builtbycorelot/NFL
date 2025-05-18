#!/usr/bin/env python3
"""Simple CLI for working with NodeForm Language (NFL) files."""

import argparse
import json
import os
import sys

from . import nfl_to_openapi


def load_json(path: str):
    """Load a JSON file from *path*."""
    with open(path, 'r', encoding='utf-8') as fh:
        return json.load(fh)


def validate_file(nfl_path: str, schema_path: str) -> bool:
    """Validate *nfl_path* against *schema_path*.

    Returns ``True`` if the file is valid, otherwise ``False``.
    This implementation performs a minimal structural validation matching the
    provided schema.
    """
    try:
        nfl = load_json(nfl_path)
    except Exception as exc:  # broad exception for CLI feedback
        print(f"Failed to load '{nfl_path}': {exc}")
        return False

    try:
        schema = load_json(schema_path)
    except Exception as exc:
        print(f"Failed to load schema '{schema_path}': {exc}")
        return False

    # minimal manual validation since jsonschema is unavailable
    if not isinstance(nfl, dict):
        print("NFL file must be a JSON object")
        return False

    if "pack" not in nfl or not isinstance(nfl["pack"], str):
        print("'pack' property missing or not a string")
        return False

    if "nodes" in nfl:
        if not isinstance(nfl["nodes"], list):
            print("'nodes' must be a list")
            return False
        for node in nfl["nodes"]:
            if not isinstance(node, dict):
                print("each node must be an object")
                return False
            if "name" not in node or "type" not in node:
                print("node entries require 'name' and 'type'")
                return False

    if "edges" in nfl:
        if not isinstance(nfl["edges"], list):
            print("'edges' must be a list")
            return False
        for edge in nfl["edges"]:
            if not isinstance(edge, dict):
                print("each edge must be an object")
                return False
            if "from" not in edge or "to" not in edge:
                print("edge entries require 'from' and 'to'")
                return False

    return True


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate an NFL JSON file against the reference schema",
    )
    parser.add_argument(
        "file",
        help="Path to the NFL JSON file",
    )
    parser.add_argument(
        "--schema",
        default=os.path.join(os.path.dirname(__file__), "..", "schema", "nfl.schema.json"),
        help="Path to the NFL JSON Schema (default: %(default)s)",
    )
    parser.add_argument(
        "--export-openapi",
        metavar="FILE",
        help="Write an OpenAPI specification to FILE",
    )

    args = parser.parse_args(argv)

    valid = validate_file(args.file, args.schema)
    if valid:
        print(f"{args.file} is valid.")
        if args.export_openapi:
            spec = nfl_to_openapi.convert_file(args.file)
            with open(args.export_openapi, "w", encoding="utf-8") as fh:
                json.dump(spec, fh, indent=2)
            print(f"OpenAPI written to {args.export_openapi}")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
