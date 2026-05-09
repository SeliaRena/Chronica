from src.chronica.domain.models import (
    Session,
    SessionHistory,
    AppUsageReport,
    TrackingRecord
)

from src.chronica.storage.sqlite.rows import SessionRow, TrackingRecordRow

class SessionRowMapper:
    @staticmethod
    def to_row(session: Session, record_id: int) -> SessionRow:
        return SessionRow(
            id=None,
            record_id=record_id,
            session_seq=session.seq,
            start_ts_ms=session.start_ts_ms,
            end_ts_ms=session.end_ts_ms,
            app_name=session.app_name,
            app_path=session.app_path,
            window_title=session.window_title,
        )

    @staticmethod
    def to_domain(row: SessionRow) -> Session:
        return Session(
            seq=row.session_seq,
            start_ts_ms=row.start_ts_ms,
            end_ts_ms=row.end_ts_ms,
            app_name=row.app_name,
            app_path=row.app_path,
            window_title=row.window_title,
        )

class TrackingRecordMapper:
    @staticmethod
    def compose_domain(
        record_row: TrackingRecordRow,
        session_rows: list[SessionRow],
    ) -> TrackingRecord:
        session_history = SessionHistory()
        app_usage_report = AppUsageReport()

        for row in sorted(session_rows, key=lambda r: r.session_seq):
            session = SessionRowMapper.to_domain(row)
            session_history.append(session)
            app_usage_report.add_session(session)

        return TrackingRecord(
            title=record_row.title,
            description=record_row.description,
            generated_at_ts_ms=record_row.generated_at_ts_ms,
            start_ts_ms=record_row.start_ts_ms,
            end_ts_ms=record_row.end_ts_ms,
            app_usage_report=app_usage_report,
            session_history=session_history,
        )