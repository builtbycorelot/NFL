from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI

from .routes import router

app = FastAPI(title="NFL API")
app.include_router(router)

# generate OpenAPI spec at import time
spec = app.openapi()
doc_path = Path(__file__).parent / "docs" / "openapi.json"
doc_path.write_text(json.dumps(spec, indent=2), encoding="utf-8")
