from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from collections.abc import Iterator

class ChronicaDatabase:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(exist_ok=True, parents=True)
        
        self._conn = sqlite3.connect(db_path)
        self._conn.row_factory = sqlite3.Row
        
        self._configure()
        
    def _configure(self) -> None:
        self._conn.execute("PRAGMA foreign_keys = ON;")
        self._conn.execute("PRAGMA journal_mode = WAL;")
        self._conn.execute("PRAGMA synchronous = NORMAL;")
    
    @property
    def connection(self) -> sqlite3.Connection:
        return self._conn
    
    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        try:
            yield self._conn
            self._conn.commit()
        except Exception:
            self._conn.rollback()
            raise
        
    def close(self) -> None:
        self._conn.close()