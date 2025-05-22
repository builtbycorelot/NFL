import json
from pathlib import Path

import cli.nfl_cli as nfl_cli

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "simple.json"
SCHEMA = Path(__file__).resolve().parents[1] / "schema" / "nfl.schema.json"


def test_validation_passes():
    """Test that validation passes for a valid NFL file."""
    assert nfl_cli.validate_file(str(EXAMPLE), str(SCHEMA))


def test_validation_fails_with_invalid_json(tmp_path):
    """Test that validation fails with invalid JSON."""
    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text("{not valid json")
    assert not nfl_cli.validate_file(str(invalid_file), str(SCHEMA))


def test_validation_fails_with_missing_schema():
    """Test that validation fails with a missing schema file."""
    assert not nfl_cli.validate_file(str(EXAMPLE), "nonexistent_schema.json")


def test_cli_export_openapi(tmp_path):
    out = tmp_path / "out.json"
    result = nfl_cli.main([str(EXAMPLE), "--export-openapi", str(out)])
    assert result == 0
    data = json.loads(out.read_text())
    assert data.get("openapi") == "3.0.0"
    assert "/nodes" in data.get("paths", {})
