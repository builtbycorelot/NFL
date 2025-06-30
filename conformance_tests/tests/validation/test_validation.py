import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from conformance_tests.src.ngl_validator import NGLValidator


def test_duplicate_node_id():
    validator = NGLValidator()
    nodes = [{"id": "n1"}, {"id": "n1"}]
    result = validator.validate(nodes)
    assert not result.valid
    assert "duplicate id: n1" in result.errors
