from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from src.chronica.domain.chronosystem import CascadedChronoSpan
from src.chronica.common.timestamp import TimestampContext

from src.chronica.domain.models import (
    Session,
    SessionHistory,
    AppUsageInfo,
    AppUsageReport,
    TrackingRecord
)

@dataclass(frozen=True, slots=True)
class SessionDisplay:
    start: datetime
    end: datetime
    duration: CascadedChronoSpan
    app_name: str
    app_path: str
    window_title: str
    
    @classmethod
    def from_session(cls, session: Session, ts_ctx: TimestampContext) -> SessionDisplay:
        return cls(
            start=ts_ctx.datetime_from_ts_ms(session.start_ts_ms),
            end=ts_ctx.datetime_from_ts_ms(session.end_ts_ms),
            duration=CascadedChronoSpan.from_total_ms(session.duration),
            app_name=session.app_name,
            app_path=session.app_path,
            window_title=session.window_title
        )
        
@dataclass(frozen=True, slots=True)
class AppUsageInfoDisplay:
    app_name: str
    app_path: str
    total_usage_time: CascadedChronoSpan
    
    @classmethod
    def from_app_usage_info(cls, info: AppUsageInfo) -> AppUsageInfoDisplay:
        return cls(
            app_name=info.app_name,
            app_path=info.app_path,
            total_usage_time=CascadedChronoSpan.from_total_ms(info.total_usage_time_ms)
        )
        
@dataclass(frozen=True, slots=True)
class TrackingRecordDisplay:
    title: str
    start: datetime
    end: datetime
    generated_at: datetime
    duration: CascadedChronoSpan
    app_usage_report: AppUsageReport
    session_history: SessionHistory
    description: str
    
    @classmethod
    def from_tracking_record(cls, record: TrackingRecord, ts_ctx: TimestampContext) -> TrackingRecordDisplay:
        return cls(
            title=record.title,
            start=ts_ctx.datetime_from_ts_ms(record.start_ts_ms),
            end=ts_ctx.datetime_from_ts_ms(record.end_ts_ms),
            generated_at=ts_ctx.datetime_from_ts_ms(record.generated_at_ts_ms),
            duration=CascadedChronoSpan.from_total_ms(record.duration),
            app_usage_report=record.app_usage_report,
            session_history=record.session_history,
            description=record.description
        )