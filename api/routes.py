from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException

from nfl import Graph
from nfl_converters import to_jsonld, to_owl, to_geojson

router = APIRouter()
_current: Graph | None = None


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/import")
def import_graph(graph: dict) -> dict:
    global _current
    try:
        _current = Graph.from_dict(graph)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"imported": True}


@router.get("/nodes")
def get_nodes() -> List[dict]:
    if _current is None:
        return []
    return [Graph._node_to_dict(n) for n in _current.nodes]


@router.get("/edges")
def get_edges() -> List[dict]:
    if _current is None:
        return []
    return [Graph._edge_to_dict(e) for e in _current.edges]


def _export_data() -> dict:
    if _current is None:
        raise HTTPException(status_code=404, detail="No graph loaded")
    return _current.to_dict()


@router.get("/export/jsonld")
def export_jsonld() -> dict:
    return to_jsonld(_export_data())


@router.get("/export/owl")
def export_owl() -> dict:
    return {"ttl": to_owl(_export_data())}


@router.get("/export/geojson")
def export_geojson() -> dict:
    return to_geojson(_export_data())
