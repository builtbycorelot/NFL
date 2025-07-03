from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class SemanticLedger:
    def __init__(self, path: str = "ledger.jsonl"):
        self.path = Path(path)

    def record(self, node_id: str, cost: float, extra: Any | None = None) -> None:
        entry = {
            "node": node_id,
            "cost": cost,
            "time": datetime.utcnow().isoformat(),
        }
        if extra is not None:
            entry["extra"] = extra
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry) + "\n")
