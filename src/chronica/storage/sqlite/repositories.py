from __future__ import annotations

import sqlite3
import src.chronica.common.timestamp as timestamp

from src.chronica.domain.models import TrackingRecord
from src.chronica.storage.sqlite.database import ChronicaDatabase
from src.chronica.storage.sqlite.rows import TrackingRecordRow, SessionRow
from src.chronica.storage.sqlite.mappers import (
    SessionRowMapper,
    TrackingRecordMapper,
)

class TrackingRecordRepository:
    def __init__(self, db: ChronicaDatabase):
        self._db = db

    def save(self, record: TrackingRecord) -> int:
        created_at_ts_ms = timestamp.now_ts_ms()

        with self._db.transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO tracking_records (
                    title,
                    description,
                    generated_at_ts_ms,
                    start_ts_ms,
                    end_ts_ms,
                    created_at_ts_ms
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    record.title,
                    record.description,
                    record.generated_at_ts_ms,
                    record.start_ts_ms,
                    record.end_ts_ms,
                    created_at_ts_ms,
                ),
            )

            record_id = int(cursor.lastrowid)

            session_rows = [
                SessionRowMapper.to_row(session, record_id)
                for session in record.session_history.chronological_sessions
            ]

            conn.executemany(
                """
                INSERT INTO sessions (
                    record_id,
                    session_seq,
                    start_ts_ms,
                    end_ts_ms,
                    app_name,
                    app_path,
                    window_title
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        row.record_id,
                        row.session_seq,
                        row.start_ts_ms,
                        row.end_ts_ms,
                        row.app_name,
                        row.app_path,
                        row.window_title,
                    )
                    for row in session_rows
                ],
            )

            return record_id

    def get(self, record_id: int) -> TrackingRecord | None:
        with self._db.transaction() as conn:
            record_raw = conn.execute(
                """
                SELECT *
                FROM tracking_records
                WHERE id = ?
                """,
                (record_id,),
            ).fetchone()

            if record_raw is None:
                return None

            session_raws = conn.execute(
                """
                SELECT *
                FROM sessions
                WHERE record_id = ?
                ORDER BY session_seq ASC
                """,
                (record_id,),
            ).fetchall()

        record_row = self._tracking_record_row_from_sqlite(record_raw)
        session_rows = [
            self._session_row_from_sqlite(row)
            for row in session_raws
        ]

        return TrackingRecordMapper.compose_domain(record_row, session_rows)
    
    def get_by_ts_ms_range(self, start_ts_ms: int, end_ts_ms: int) -> list[TrackingRecord]:
        res: list[TrackingRecord] = []
        
        with self._db.transaction() as conn:
            record_raws = conn.execute(
                """
                SELECT *
                FROM tracking_records
                WHERE start_ts_ms >= ? AND end_ts_ms <= ?
                ORDER BY start_ts_ms DESC
                """,
                (start_ts_ms, end_ts_ms),
            ).fetchall()
            
            for record_raw in record_raws:
                record_row = self._tracking_record_row_from_sqlite(record_raw)
                session_raws = conn.execute(
                    """
                    SELECT *
                    FROM sessions
                    WHERE record_id = ?
                    ORDER BY session_seq ASC
                    """,
                    (record_row.id,),
                ).fetchall()
                
                session_rows = [
                    self._session_row_from_sqlite(row)
                    for row in session_raws
                ]
                
                res.append(TrackingRecordMapper.compose_domain(record_row, session_rows))

        return res
    
    def get_all(self) -> list[TrackingRecord]:
        res: list[TrackingRecord] = []
        record_rows = self.list_record_rows()
        
        for record_row in record_rows:
            with self._db.transaction() as conn:
                session_raws = conn.execute(
                    """
                    SELECT *
                    FROM sessions
                    WHERE record_id = ?
                    ORDER BY session_seq ASC
                    """,
                    (record_row.id,),
                ).fetchall()
                
                session_rows = [
                    self._session_row_from_sqlite(row)
                    for row in session_raws
                ]
                
                res.append(TrackingRecordMapper.compose_domain(record_row, session_rows))
        
        return res

    def list_record_rows(self) -> list[TrackingRecordRow]:
        with self._db.transaction() as conn:
            rows = conn.execute(
                """
                SELECT *
                FROM tracking_records
                ORDER BY start_ts_ms DESC
                """
            ).fetchall()

        return [self._tracking_record_row_from_sqlite(row) for row in rows]

    def delete(self, record_id: int) -> None:
        with self._db.transaction() as conn:
            conn.execute(
                """
                DELETE FROM tracking_records
                WHERE id = ?
                """,
                (record_id,),
            )

    def delete_by_title(self, record_title: str) -> None:
        with self._db.transaction() as conn:
            conn.execute(
                """
                DELETE FROM tracking_records
                WHERE title = ?
                """,
                (record_title,),
            )

    @staticmethod
    def _tracking_record_row_from_sqlite(row: sqlite3.Row) -> TrackingRecordRow:
        return TrackingRecordRow(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            generated_at_ts_ms=row["generated_at_ts_ms"],
            start_ts_ms=row["start_ts_ms"],
            end_ts_ms=row["end_ts_ms"],
            created_at_ts_ms=row["created_at_ts_ms"],
        )

    @staticmethod
    def _session_row_from_sqlite(row: sqlite3.Row) -> SessionRow:
        return SessionRow(
            id=row["id"],
            record_id=row["record_id"],
            session_seq=row["session_seq"],
            start_ts_ms=row["start_ts_ms"],
            end_ts_ms=row["end_ts_ms"],
            app_name=row["app_name"],
            app_path=row["app_path"],
            window_title=row["window_title"],
        )