from src.chronica.domain.models.session import Session
from src.chronica.domain.models.session_history import SessionHistory

class WindowUsageInfo:
    def __init__(self, window_title: str, 
                 session_history: SessionHistory | None = None,
                 total_usage_time_ms: int = 0):
        self.window_title = window_title
        self.session_history = session_history if session_history is not None else SessionHistory()
        self.total_usage_time_ms: int = total_usage_time_ms
    
    def add_session(self, session: Session) -> None:
        self.session_history.append(session)
        self.total_usage_time_ms += session.duration
    
    @property
    def focus_count(self) -> int:
        return len(self.session_history)
    
    @property
    def last_used_ts_ms(self) -> int | None:
        if self.session_history.is_empty:
            return None
        
        return self.session_history.latest.end_ts_ms
    
    @property
    def peak_usage_session(self) -> Session | None:
        if self.session_history.is_empty:
            return None
        
        return max(self.session_history.chronological_sessions, key=lambda s: s.duration)
    
    def to_debug_dict(self) -> dict:
        return {
            "window_title": self.window_title,
            "total_usage_time_ms": self.total_usage_time_ms,
            "session_history": self.session_history.to_debug_list()
        }