from src.chronica.domain.models.session import Session
from src.chronica.domain.models.session_history import SessionHistory
from src.chronica.domain.models.window_usage_info import WindowUsageInfo

class AppUsageInfo:
    def __init__(self, app_name: str,
                 app_path: str,
                 window_usage_map: dict[str, WindowUsageInfo] | None = None,
                 total_usage_time_ms: int = 0) -> None:
        self.app_name: str = app_name
        self.app_path: str = app_path
        self.window_usage_map: dict[str, WindowUsageInfo] = window_usage_map if window_usage_map is not None else {}
        self.total_usage_time_ms: int = total_usage_time_ms
    
    def add_session(self, session: Session) -> None:
        if session.window_title not in self.window_usage_map:
            self.window_usage_map[session.window_title] = WindowUsageInfo(session.window_title)
        
        self.window_usage_map[session.window_title].add_session(session)
        self.total_usage_time_ms += session.duration

    @property
    def session_count(self) -> int:
        return sum(w.session_count for w in self.window_usage_map.values())
    
    @property
    def window_count(self) -> int:
        return len(self.window_usage_map)
    
    @property
    def app_entry_count(self) -> int:
        sorted_merged_history = SessionHistory(
            sorted(
                (
                    s
                    for w in self.window_usage_map.values()
                    for s in w.session_history.chronological_sessions
                ),
                key=lambda s: s.start_ts_ms
            )
        )
        
        return sorted_merged_history.contiguous_segment_count
    
    @property
    def first_used_ts_ms(self) -> int:
        return min(wu.first_used_ts_ms for wu in self.window_usage_map.values())
    
    @property
    def last_used_ts_ms(self) -> int:
        return max(wu.last_used_ts_ms for wu in self.window_usage_map.values())
    
    def to_debug_dict(self) -> dict:
        return {
            "app_name": self.app_name,
            "total_usage_time_ms": self.total_usage_time_ms,
            "window_usage_map": {window_title: window_usage_info.to_debug_dict() for window_title, window_usage_info in self.window_usage_map.items()}
        }