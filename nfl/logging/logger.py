from __future__ import annotations

import json
import logging
from pathlib import Path


class JsonLogger(logging.Logger):
    """Logger that emits JSON lines."""

    def __init__(self, name: str, log_file: str = "nfl.log") -> None:
        super().__init__(name)
        handler = logging.FileHandler(Path(log_file))
        handler.setFormatter(_JsonFormatter())
        self.addHandler(handler)
        self.setLevel(logging.INFO)


class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
        payload = {
            "level": record.levelname,
            "msg": record.getMessage(),
            "time": self.formatTime(record),
        }
        return json.dumps(payload)
