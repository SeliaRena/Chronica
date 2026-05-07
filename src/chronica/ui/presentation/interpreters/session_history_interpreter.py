from src.chronica.common.timestamp import TimestampContextProvider
from src.chronica.ui.presentation.settings import (
    SessionTimelineGroupingMode,
    SessionTimelineRowSorting,
    SessionTimelineSettings
)

from src.chronica.ui.presentation.models import (
    SessionDisplay,
    SessionTimelineSegment,
    SessionTimelineRow,
    SessionTimeline
)

from src.chronica.domain.models import (
    Session,
    SessionHistory
)

import hashlib

class _SessionTimelineKeyGenerator:
    def __init__(self, settings: SessionTimelineSettings):
        self.settings = settings
        
    @staticmethod
    def _stable_key(*parts: object) -> str:
        raw = "|".join(str(p) for p in parts)
        return hashlib.blake2b(raw.encode("utf-8"), digest_size=8).hexdigest()
    
    def generate_segment_key(self, session: Session) -> str:
        return self._stable_key(
            "session-timeline-segment",
            session.app_name,
            session.window_title,
            session.start_ts_ms,
            session.end_ts_ms
        )
        
    def generate_segment_color_key(self, session: Session) -> str:
        return self._stable_key(
            "session-timeline-segment-color-by-app",
            session.app_name
        )
        
    def generate_row_key(self, session: Session) -> str:
        grp_mode = self.settings.grouping_mode
        
        if grp_mode == SessionTimelineGroupingMode.BY_APP:
            return self._stable_key(
                "session-timeline-row-by-app",
                session.app_name
            )
        if grp_mode == SessionTimelineGroupingMode.BY_WINDOW:
            return self._stable_key(
                "session-timeline-row-by-window",
                session.app_name,
                session.window_title
            )
        
        raise ValueError(f"Unknown grouping mode: {grp_mode}")

class SessionHistoryInterpreter:
    def __init__(self, ts_ctx_provider: TimestampContextProvider, settings: SessionTimelineSettings):
        self.ts_ctx_provider = ts_ctx_provider
        self.settings = settings
        self._keygen = _SessionTimelineKeyGenerator(settings)
        
    def _resolve_row_label(self, sd: SessionDisplay) -> str:
        grp_mode = self.settings.grouping_mode
        
        if grp_mode == SessionTimelineGroupingMode.BY_APP:
            return sd.app_name
        if grp_mode == SessionTimelineGroupingMode.BY_WINDOW:
            return f"{sd.app_name} - {sd.window_title}"
        
        raise ValueError(f"Unknown grouping mode: {grp_mode}")
    
    def _sorted_timeline_rows(self, rows: list[SessionTimelineRow]) -> list[SessionTimelineRow]:
        row_sorting_mode = self.settings.row_sorting
        return sorted(rows, key=lambda r: r.label, reverse=row_sorting_mode == SessionTimelineRowSorting.REVERSED_ALPHABETICAL)
        
    def to_session_timeline(self, history: SessionHistory) -> SessionTimeline:
        row_map: dict[str, list[SessionTimelineSegment]] = {}
        ts_ctx = self.ts_ctx_provider.get()
        
        for session in history.chronological_sessions:
            session_display = SessionDisplay.from_session(session, ts_ctx)
            segment_key = self._keygen.generate_segment_key(session)
            row_key = self._keygen.generate_row_key(session)
            color_key = self._keygen.generate_segment_color_key(session)
            
            row_map.setdefault(row_key, []).append(SessionTimelineSegment(
                key=segment_key,
                row_key=row_key,
                session=session_display,
                color_key=color_key
            ))
        
        timeline_rows: list[SessionTimelineRow] = []
        for row_key, segments in row_map.items():
            sd = segments[0].session
            label = self._resolve_row_label(sd)
            
            timeline_rows.append(SessionTimelineRow(
                key=row_key,
                label=label,
                segments=tuple(segments)
            ))
        
        return SessionTimeline(rows=tuple(self._sorted_timeline_rows(timeline_rows)))