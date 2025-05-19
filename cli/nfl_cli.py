#!/usr/bin/env python3
"""Simple CLI for working with NodeForm Language (NFL) files."""

import argparse
import json
import os
import sys
from typing import Any

try:
    from jsonschema import validate as jsonschema_validate
    from jsonschema.exceptions import ValidationError
    _HAS_JSONSCHEMA = True
except Exception:  # pragma: no cover - dependency missing
    _HAS_JSONSCHEMA = False

    class ValidationError(Exception):
        """Fallback ValidationError when jsonschema is unavailable."""


def _fallback_validate(instance: Any, schema: Any) -> None:
    """A very small JSON Schema validator supporting the NFL schema."""

    def _error(msg: str) -> None:
        raise ValidationError(msg)

    if not isinstance(instance, dict):
        _error("NFL file must be a JSON object")

    if schema.get("type") != "object":
        _error("Schema root must be an object")

    required = schema.get("required", [])
    for key in required:
        if key not in instance:
            _error(f"Missing required property: {key}")

    properties = schema.get("properties", {})
    for key, value in instance.items():
        subschema = properties.get(key)
        if not subschema:
            continue
        if subschema.get("type") == "string" and not isinstance(value, str):
            _error(f"'{key}' must be a string")
        if subschema.get("type") == "array":
            if not isinstance(value, list):
                _error(f"'{key}' must be a list")
            item_schema = subschema.get("items", {})
            for item in value:
                if item_schema.get("type") == "object" and not isinstance(item, dict):
                    _error(f"items of '{key}' must be objects")
                if isinstance(item, dict):
                    req = item_schema.get("required", [])
                    for r in req:
                        if r not in item:
                            _error(f"Missing required property in {key}: {r}")

    return None

from . import nfl_to_openapi


def load_json(path: str):
    """Load a JSON file from *path*."""
    with open(path, 'r', encoding='utf-8') as fh:
        return json.load(fh)


def validate_file(nfl_path: str, schema_path: str) -> bool:
    """Validate *nfl_path* against *schema_path*.

    Returns ``True`` if the file is valid, otherwise ``False``.
    Uses :mod:`jsonschema` when available and falls back to a very small
    validator that covers the shipped schema.
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
        if _HAS_JSONSCHEMA:
            jsonschema_validate(instance=nfl, schema=schema)
        else:
            _fallback_validate(nfl, schema)
    except ValidationError as exc:
        print(f"Validation error: {exc}")
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
