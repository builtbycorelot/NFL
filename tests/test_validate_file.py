import json
import tempfile
from pathlib import Path
import unittest

import cli.nfl_cli as cli

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"
SCHEMA = Path(__file__).resolve().parents[1] / "schema" / "nfl.schema.json"


class TestValidateFile(unittest.TestCase):
    def test_valid_examples(self):
        for path in EXAMPLES.glob("*.json"):
            self.assertTrue(cli.validate_file(str(path), str(SCHEMA)), f"{path} should be valid")

    def test_missing_pack(self):
        data = json.loads((EXAMPLES / "simple.json").read_text())
        data.pop("pack", None)
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_file = Path(tmpdir) / "invalid.json"
            tmp_file.write_text(json.dumps(data))
            self.assertFalse(cli.validate_file(str(tmp_file), str(SCHEMA)))


if __name__ == "__main__":
    unittest.main()
