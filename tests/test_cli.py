import json
import os
from cli import nfl_cli

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), '..', 'schema', 'nfl.schema.json')
VALID_PATH = os.path.join(os.path.dirname(__file__), '..', 'examples', 'simple.json')


def test_validate_file_success():
    assert nfl_cli.validate_file(VALID_PATH, SCHEMA_PATH)


def test_validate_file_invalid(tmp_path):
    invalid = tmp_path / 'invalid.json'
    invalid.write_text(json.dumps({'nodes': []}))
    assert not nfl_cli.validate_file(str(invalid), SCHEMA_PATH)


def test_cli_success(capsys):
    exit_code = nfl_cli.main([VALID_PATH, '--schema', SCHEMA_PATH])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert 'is valid' in captured.out


def test_cli_invalid(tmp_path, capsys):
    invalid = tmp_path / 'invalid.json'
    invalid.write_text(json.dumps({'nodes': []}))
    exit_code = nfl_cli.main([str(invalid), '--schema', SCHEMA_PATH])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert 'Validation error' in captured.out
# (The merge conflict marker and the old test definitions have been removed)
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

