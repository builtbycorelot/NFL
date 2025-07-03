import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
)
from conformance_tests.src.ngl_executor import NGLExecutor


def dummy_func(x, y):
    return x + y


def test_python_execution():
    executor = NGLExecutor()
    result = executor.execute(dummy_func, 2, 3)
    assert result.success
    assert result.output == 5
    assert result.errors == []
