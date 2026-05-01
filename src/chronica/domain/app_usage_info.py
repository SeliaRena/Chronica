from src.chronica.domain.session import Session
from src.chronica.domain.window_usage_info import WindowUsageInfo

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
    def focus_count(self) -> int:
        return sum(window_usage_info.focus_count for window_usage_info in self.window_usage_map.values())
    
    @property
    def last_used_window(self) -> WindowUsageInfo | None:
        if not self.window_usage_map:
            return None
        
        return max(self.window_usage_map.values(), key=lambda w: w.last_used_ts_ms or 0)
    
    @property
    def peak_total_usage_window(self) -> WindowUsageInfo | None:
        if not self.window_usage_map:
            return None
        
        return max(self.window_usage_map.values(), key=lambda w: w.total_usage_time_ms)
    
    @property
    def peak_single_time_usage_window(self) -> WindowUsageInfo | None:
        if not self.window_usage_map:
            return None
        
        return max(self.window_usage_map.values(), key=lambda w: w.peak_usage_session.duration if w.peak_usage_session else 0)
    
    def to_debug_dict(self) -> dict:
        return {
            "app_name": self.app_name,
            "total_usage_time_ms": self.total_usage_time_ms,
            "window_usage_map": {window_title: window_usage_info.to_debug_dict() for window_title, window_usage_info in self.window_usage_map.items()}
        }