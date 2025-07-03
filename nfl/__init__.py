"""Core NFL package."""

from .graph import Graph, Node, Edge, validate_graph
from .executor import Executor
from .distributed.executor import DistributedExecutor
from .storage.arrow_store import ArrowStore
from .storage.index import AttributeIndex
from .logging.logger import JsonLogger
from .logging.errors import NFLError
from .ledger import SemanticLedger
from .cost_model import CostModel
from .converters import to_jsonld, to_owl

__all__ = [
    "Graph",
    "Node",
    "Edge",
    "validate_graph",
    "Executor",
    "DistributedExecutor",
    "ArrowStore",
    "AttributeIndex",
    "JsonLogger",
    "NFLError",
    "SemanticLedger",
    "CostModel",
    "to_jsonld",
    "to_owl",
]

# Optional imports
try:  # pragma: no cover - optional dependency may not be installed
    from .storage.postgres_store import PostgresStore
except Exception:  # pragma: no cover - library may be missing
    PostgresStore = None
else:
    __all__.append("PostgresStore")

try:  # pragma: no cover - optional dependency may not be installed
    from .storage.neo4j_store import Neo4jStore
except Exception:  # pragma: no cover - library may be missing
    Neo4jStore = None
else:
    __all__.append("Neo4jStore")

try:  # pragma: no cover - optional dependency may not be installed
    from nfl_converters import to_geojson as _to_geojson
except Exception:  # pragma: no cover - library may be missing
    pass
else:
    to_geojson = _to_geojson
    __all__.append("to_geojson")
