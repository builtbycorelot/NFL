import json
from cli import nfl_to_openapi


def test_openapi_paths():
    spec = nfl_to_openapi.convert_file('index.nfl.json')
    assert '/nodes' in spec['paths']
    assert '/edges' in spec['paths']
