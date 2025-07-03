import pytest
from nfl.graph import Graph, Node
from nfl.executor import Executor

pytest.importorskip("pytest_benchmark")


@pytest.fixture
def graph():
    import os

    scale = int(os.getenv("NFL_BENCH_SCALE", "100"))
    nodes = [Node(name=f"n{i}", type="X") for i in range(scale)]
    edges = []
    return Graph(pack="bench", nodes=nodes, edges=edges)


def test_execute_speed(benchmark, graph):
    executor = Executor(graph)
    benchmark(lambda: executor.execute("n0"))
