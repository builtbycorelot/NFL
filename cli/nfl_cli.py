#!/usr/bin/env python3
"""Simple CLI for working with NodeForm Language (NFL) files."""

import argparse
import json
import os

import jsonschema

from . import nfl_to_openapi
from . import nfl_to_semantics


def load_json(path: str):
    """Load a JSON file from *path*.

    Any :class:`OSError` encountered while opening the file or
    :class:`json.JSONDecodeError` raised during parsing is re-raised with
    additional context describing the path being processed.
    """
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except OSError as exc:
        raise IOError(f"Failed to read '{path}': {exc}") from exc
    except json.JSONDecodeError as exc:
        raise json.JSONDecodeError(
            f"Invalid JSON in '{path}': {exc.msg}", exc.doc, exc.pos
        ) from exc


def validate_file(nfl_path: str, schema_path: str) -> bool:
    """Validate *nfl_path* against *schema_path*.

    Returns ``True`` if the file is valid, otherwise ``False``.
    Validation uses ``jsonschema`` to ensure the file matches the schema.
    """
    try:
        nfl = load_json(nfl_path)
    except IOError as exc:
        print(exc)
        return False
    except json.JSONDecodeError as exc:
        print(exc)
        return False

    try:

        schema = load_json(schema_path)
    except IOError as exc:
        print(exc)
        return False
    except json.JSONDecodeError as exc:
        print(exc)
=======
        load_json(schema_path)
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
    parser.add_argument(
        "--export-jsonld",
        metavar="FILE",
        help="Write a JSON-LD graph to FILE",
    )
    parser.add_argument(
        "--export-owl",
        metavar="FILE",
        help="Write an OWL/Turtle representation to FILE",
    )
    parser.add_argument(
        "--export-geojson",
        metavar="FILE",
        help="Write a GeoJSON file to FILE",
    )
    parser.add_argument(
        "--export-ifc",
        metavar="FILE",
        help="Write an IFC text representation to FILE",
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
        if any([args.export_jsonld, args.export_owl, args.export_geojson, args.export_ifc]):
            converted = nfl_to_semantics.convert_file(args.file)
            if args.export_jsonld:
                with open(args.export_jsonld, "w", encoding="utf-8") as fh:
                    json.dump(converted["jsonld"], fh, indent=2)
                print(f"JSON-LD written to {args.export_jsonld}")
            if args.export_owl:
                with open(args.export_owl, "w", encoding="utf-8") as fh:
                    fh.write(converted["owl"])
                print(f"OWL written to {args.export_owl}")
            if args.export_geojson:
                with open(args.export_geojson, "w", encoding="utf-8") as fh:
                    json.dump(converted["geojson"], fh, indent=2)
                print(f"GeoJSON written to {args.export_geojson}")
            if args.export_ifc:
                with open(args.export_ifc, "w", encoding="utf-8") as fh:
                    fh.write(converted["ifc"])
                print(f"IFC written to {args.export_ifc}")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
