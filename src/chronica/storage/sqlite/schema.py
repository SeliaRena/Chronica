from src.chronica.storage.sqlite.database import ChronicaDatabase

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS tracking_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT 'no description',

    generated_at_ts_ms INTEGER NOT NULL,
    start_ts_ms INTEGER NOT NULL,
    end_ts_ms INTEGER NOT NULL,

    created_at_ts_ms INTEGER NOT NULL,

    CHECK (end_ts_ms >= start_ts_ms)
);

CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    record_id INTEGER NOT NULL,
    session_seq INTEGER NOT NULL,

    start_ts_ms INTEGER NOT NULL,
    end_ts_ms INTEGER NOT NULL,

    app_name TEXT NOT NULL,
    app_path TEXT NOT NULL,
    window_title TEXT NOT NULL,

    FOREIGN KEY (record_id)
        REFERENCES tracking_records(id)
        ON DELETE CASCADE,

    UNIQUE (record_id, session_seq),

    CHECK (end_ts_ms >= start_ts_ms)
);

CREATE INDEX IF NOT EXISTS idx_sessions_record_seq
ON sessions(record_id, session_seq);

CREATE INDEX IF NOT EXISTS idx_sessions_time_range
ON sessions(start_ts_ms, end_ts_ms);

CREATE INDEX IF NOT EXISTS idx_sessions_app_name
ON sessions(app_name);

CREATE INDEX IF NOT EXISTS idx_sessions_record_app
ON sessions(record_id, app_name);
"""

def initialize_schema(db: ChronicaDatabase) -> None:
    db.connection.executescript(SCHEMA_SQL)
    db.connection.commit()