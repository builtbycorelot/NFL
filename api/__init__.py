from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI

from .routes import router

app = FastAPI(title="NFL API")

# serve a simple landing page linking to documentation

@app.get("/")
def index() -> str:
    """Landing page with helpful links."""
    return """
    <html>
      <body>
        <h1>NFL API</h1>
        <ul>
          <li><a href=\"/docs\">Swagger UI</a></li>
          <li><a href=\"/redoc\">ReDoc</a></li>
          <li><a href=\"/openapi.json\">OpenAPI JSON</a></li>
          <li><a href=\"/health\">Health Check</a></li>
          <li><a href=\"https://github.com/builtbycorelot/NFL/tree/main/docs/site\">Docs Site</a></li>
        </ul>
      </body>
    </html>
    """

app.include_router(router)

# generate OpenAPI spec at import time
spec = app.openapi()
doc_path = Path(__file__).parent / "docs" / "openapi.json"
doc_path.write_text(json.dumps(spec, indent=2), encoding="utf-8")
