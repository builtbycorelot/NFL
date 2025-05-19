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
