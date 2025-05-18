"""Convert NFL JSON graphs to a minimal OpenAPI specification."""

from __future__ import annotations

import json
from typing import Any, Dict


def convert(nfl: Dict[str, Any]) -> Dict[str, Any]:
    """Return a dictionary representing an OpenAPI spec for *nfl*."""
    nodes = nfl.get("nodes", [])
    edges = nfl.get("edges", [])

    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": f"NFL Graph - {nfl.get('pack', '')}",
            "version": "1.0.0",
        },
        "paths": {
            "/nodes": {
                "get": {
                    "summary": "List nodes",
                    "responses": {
                        "200": {
                            "description": "List of nodes",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Node"},
                                    },
                                    "example": nodes,
                                }
                            },
                        }
                    },
                }
            },
            "/edges": {
                "get": {
                    "summary": "List edges",
                    "responses": {
                        "200": {
                            "description": "List of edges",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Edge"},
                                    },
                                    "example": edges,
                                }
                            },
                        }
                    },
                }
            },
        },
        "components": {
            "schemas": {
                "Node": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                    },
                },
                "Edge": {
                    "type": "object",
                    "properties": {
                        "from": {"type": "string"},
                        "to": {"type": "string"},
                    },
                },
            }
        },
    }

    return spec


def convert_file(path: str) -> Dict[str, Any]:
    """Load the NFL file at *path* and convert it to OpenAPI."""
    with open(path, "r", encoding="utf-8") as fh:
        nfl = json.load(fh)
    return convert(nfl)


__all__ = ["convert", "convert_file"]
