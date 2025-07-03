from __future__ import annotations

from . import FastAPI, HTTPException


class Response:
    def __init__(self, data, status_code: int = 200):
        self._data = data
        self.status_code = status_code

    def json(self):
        return self._data


class TestClient:
    def __init__(self, app: FastAPI) -> None:
        self.app = app

    def get(self, path: str) -> Response:
        try:
            data = self.app._call_route("GET", path)
            return Response(data, 200)
        except HTTPException as e:
            return Response({"detail": e.detail}, e.status_code)

    def post(self, path: str, json=None) -> Response:
        try:
            data = self.app._call_route("POST", path, json=json)
            return Response(data, 200)
        except HTTPException as e:
            return Response({"detail": e.detail}, e.status_code)
