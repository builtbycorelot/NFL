import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from nfl.parser import parse_nfl
from jsonschema import Draft202012Validator
import json

SCHEMA = json.load(open("schema/nfl.schema.json"))
NFL_FILES = pathlib.Path(".").glob("**/*.nfl")


def test_nfl_files():
    for path in NFL_FILES:
        ast = parse_nfl(path.read_text())
        Draft202012Validator(SCHEMA).validate(ast)
