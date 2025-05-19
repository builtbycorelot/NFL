#!/usr/bin/env python3
"""Simple CLI for working with NodeForm Language (NFL) files."""

import argparse
import json
import os
import sys

import jsonschema

from . import nfl_to_openapi


def load_json(path: str):
    """Load a JSON file from *path*."""
    with open(path, 'r', encoding='utf-8') as fh:
        return json.load(fh)


def validate_file(nfl_path: str, schema_path: str) -> bool:
    """Validate *nfl_path* against *schema_path*.

    Returns ``True`` if the file is valid, otherwise ``False``.
    Validation uses ``jsonschema`` to ensure the file matches the schema.
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

    try:
        jsonschema.validate(nfl, schema)
    except jsonschema.ValidationError as exc:
        print(f"Validation error: {exc.message}")
        return False
    except jsonschema.SchemaError as exc:
        print(f"Invalid schema: {exc}")
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
