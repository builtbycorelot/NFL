import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
)
from conformance_tests.src.ngl_storage import NGLStorage


def test_store_and_retrieve_nodes():
    storage = NGLStorage()
    storage.store_nodes([{"id": "n1"}])
    nodes = storage.get_nodes()
    assert nodes == [{"id": "n1"}]
