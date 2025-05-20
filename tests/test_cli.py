import json
from pathlib import Path

import cli.nfl_cli as nfl_cli

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "simple.json"
SCHEMA = Path(__file__).resolve().parents[1] / "schema" / "nfl.schema.json"


def test_validation_passes():
    assert nfl_cli.validate_file(str(EXAMPLE), str(SCHEMA))


def test_cli_export_openapi(tmp_path):
    out = tmp_path / "out.json"
    result = nfl_cli.main([str(EXAMPLE), "--export-openapi", str(out)])
    assert result == 0
    data = json.loads(out.read_text())
    assert data.get("openapi") == "3.0.0"
    assert "/nodes" in data.get("paths", {})
