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
    def session_count(self) -> int:
        return len(self.session_history)
    
    @property
    def first_used_ts_ms(self) -> int:
        """
        Returns the start timestamp of the oldest session in the history \n
        This property assumes that the session history is not empty, and raises ValueError if the session history is empty
        """
        
        return self.session_history.require_oldest.start_ts_ms
    
    @property
    def last_used_ts_ms(self) -> int:
        """
        Returns the end timestamp of the latest session in the history \n
        This property assumes that the session history is not empty, and raises ValueError if the session history is empty
        """
        
        return self.session_history.require_latest.end_ts_ms
    
    @property
    def peak_usage_session(self) -> Session:
        return max(self.session_history.chronological_sessions, key=lambda s: s.duration)
    
    @property
    def peak_gap_duration_ms(self) -> int:
        sessions = self.session_history.chronological_sessions
        ret = 0
        
        for i, s in enumerate(sessions):
            if i > 0:
                ret = max(ret, s.start_ts_ms - sessions[i - 1].end_ts_ms)
        
        return ret
    
    @property
    def avg_session_duration_ms(self) -> int:
        return self.total_usage_time_ms // len(self.session_history)
    
    def to_debug_dict(self) -> dict:
        return {
            "window_title": self.window_title,
            "total_usage_time_ms": self.total_usage_time_ms,
            "session_history": self.session_history.to_debug_list()
        }