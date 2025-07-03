import sqlite3
from contextlib import contextmanager

class extras:
    class RealDictCursor(sqlite3.Cursor):
        pass

class _Connection(sqlite3.Connection):
    def cursor(self, cursor_factory=None):
        cur = super().cursor()
        if cursor_factory is extras.RealDictCursor:
            self.row_factory = sqlite3.Row
        return cur

def connect(dsn):
    return _Connection(':memory:')

__all__ = ['connect', 'extras']
__version__ = 'stub'
