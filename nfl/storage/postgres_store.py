from __future__ import annotations

from typing import Any, Iterable

try:
    import psycopg2
except Exception:  # pragma: no cover - offline stub
    from offline_stubs import psycopg2


class PostgresStore:
    """Very small wrapper around psycopg2 for demo purposes."""

    def __init__(self, dsn: str) -> None:
        self.dsn = dsn
        self.conn = psycopg2.connect(dsn)

    def execute(self, sql: str, params: Iterable[Any] | None = None) -> None:
        cur = self.conn.cursor()
        cur.execute(sql, params or [])
        self.conn.commit()
        cur.close()

    def query(self, sql: str, params: Iterable[Any] | None = None) -> list[tuple[Any, ...]]:
        cur = self.conn.cursor()
        cur.execute(sql, params or [])
        rows = cur.fetchall()
        cur.close()
        return rows
