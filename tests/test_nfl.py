import json
import os
import sys
import tempfile
import subprocess
import unittest

from cli import nfl_cli
from cli import nfl_to_openapi

ROOT_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))
EXAMPLES_DIR = os.path.join(ROOT_DIR, "examples")
SCHEMA_PATH = os.path.join(ROOT_DIR, "schema", "nfl.schema.json")


class ValidateFileTests(unittest.TestCase):
    def test_validate_example_files(self):
        for name in os.listdir(EXAMPLES_DIR):
            path = os.path.join(EXAMPLES_DIR, name)
            with self.subTest(example=path):
                self.assertTrue(nfl_cli.validate_file(path, SCHEMA_PATH))

    def test_validate_invalid_file(self):
        with tempfile.NamedTemporaryFile("w", delete=False) as tmp:
            tmp.write("{}")
            tmp_path = tmp.name
        try:
            with self.assertRaises(Exception):
                nfl_cli.validate_file(tmp_path, SCHEMA_PATH)
        finally:
            os.remove(tmp_path)


class ConvertFileTests(unittest.TestCase):
    def test_convert_file_examples(self):
        example = os.path.join(EXAMPLES_DIR, "simple.json")
        spec = nfl_to_openapi.convert_file(example)
        with open(example, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        node_example = (
            spec["paths"]["/nodes"]["get"]["responses"]["200"]["content"]["application/json"]["example"]
        )
        edge_example = (
            spec["paths"]["/edges"]["get"]["responses"]["200"]["content"]["application/json"]["example"]
        )
        self.assertEqual(node_example, data.get("nodes", []))
        self.assertEqual(edge_example, data.get("edges", []))
        self.assertEqual(spec["openapi"], "3.0.0")


class CLITests(unittest.TestCase):
    def test_cli_export_openapi(self):
        example = os.path.join(EXAMPLES_DIR, "simple.json")
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = os.path.join(tmpdir, "out.json")
            proc = subprocess.run(
                [sys.executable, "-m", "cli.nfl_cli", example, "--export-openapi", out_path],
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0)
            self.assertIn("is valid", proc.stdout)
            self.assertTrue(os.path.exists(out_path))


if __name__ == "__main__":
    unittest.main()
