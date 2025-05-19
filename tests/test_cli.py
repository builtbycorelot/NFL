import json
from cli.nfl_cli import validate_file
from cli.nfl_to_openapi import convert_file

SCHEMA_PATH = "schema/nfl.schema.json"


def test_validate_file_valid():
    assert validate_file("examples/simple.json", SCHEMA_PATH)


def test_validate_file_invalid(tmp_path):
    invalid = tmp_path / "invalid.json"
    invalid.write_text("{}", encoding="utf-8")
    assert not validate_file(str(invalid), SCHEMA_PATH)


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

