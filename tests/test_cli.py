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
