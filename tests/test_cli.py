import json
import pytest
from cli.nfl_cli import validate_file
from cli.nfl_to_openapi import convert_file

SCHEMA_PATH = "schema/nfl.schema.json"


def test_validate_file_valid():
    assert validate_file("examples/simple.json", SCHEMA_PATH)


def test_validate_file_invalid(tmp_path):
    invalid = tmp_path / "invalid.json"
    invalid.write_text("{}", encoding="utf-8")
    with pytest.raises((ValueError, json.JSONDecodeError)):
        validate_file(str(invalid), SCHEMA_PATH)


def test_convert_file_simple():
    spec = convert_file("examples/simple.json")
    assert spec["openapi"] == "3.0.0"
    assert spec["info"]["title"] == "NFL Graph - meta.core"
    assert spec["paths"]["/nodes"]["get"]["responses"]["200"]["content"]["application/json"]["example"] == [
        {"name": "x", "type": "\u211d"},
        {"name": "y", "type": "\u211d"},
    ]
    assert spec["paths"]["/edges"]["get"]["responses"]["200"]["content"]["application/json"]["example"] == [
        {"from": "x", "to": "y"}
    ]


def test_validate_file_schema_error(tmp_path):
    missing = tmp_path / "missing.json"
    with pytest.raises(IOError):
        validate_file("examples/simple.json", str(missing))


def test_validate_stateful_example():
    assert validate_file("examples/stateful.json", SCHEMA_PATH)


def test_validate_unknown_edge(tmp_path):
    graph = {
        "pack": "bad",
        "nodes": [{"name": "a", "type": "X"}],
        "edges": [{"from": "a", "to": "b"}],
    }
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(graph), encoding="utf-8")
    with pytest.raises(ValueError):
        validate_file(str(path), SCHEMA_PATH)

