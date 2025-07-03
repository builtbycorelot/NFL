import os
import subprocess
import sys
import unittest

from nfl.graph import Graph

ROOT_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))
EXAMPLES_DIR = os.path.join(ROOT_DIR, "examples")


class ValidateFileTests(unittest.TestCase):
    def test_validate_example_files(self):
        for name in os.listdir(EXAMPLES_DIR):
            path = os.path.join(EXAMPLES_DIR, name)
            with self.subTest(example=path):
                Graph.load(path)

    def test_cli_validate(self):
        example = os.path.join(EXAMPLES_DIR, "simple.json")
        proc = subprocess.run(
            [sys.executable, "-m", "cli.nfl_cli", "validate", example],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertIn("is valid", proc.stdout)


if __name__ == "__main__":
    unittest.main()
