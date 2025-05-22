import json
import subprocess
import sys
from pathlib import Path


def test_cli_validation():
    result = subprocess.run(
        [sys.executable, "-m", "cli.nfl_cli", "examples/simple.json"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "examples/simple.json is valid." in result.stdout


def test_export_openapi(tmp_path: Path):
    out_file = tmp_path / "spec.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "cli.nfl_cli",
            "examples/simple.json",
            "--export-openapi",
            str(out_file),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0

    data = json.loads(out_file.read_text())

    expected_nodes = [
        {"name": "x", "type": "ℝ"},
        {"name": "y", "type": "ℝ"},
    ]
    expected_edges = [{"from": "x", "to": "y"}]

    nodes_example = data["paths"]["/nodes"]["get"]["responses"]["200"]["content"][
        "application/json"
    ]["example"]
    edges_example = data["paths"]["/edges"]["get"]["responses"]["200"]["content"][
        "application/json"
    ]["example"]

    assert nodes_example == expected_nodes
    assert edges_example == expected_edges
=======
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

