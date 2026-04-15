from src.chronica.domain.session import Session
from datetime import datetime

class SessionHistory:
    def __init__(self, sessions: list[Session] | None = None):
        self.chronological_sessions: list[Session] = sessions if sessions is not None else []
        
    def __len__(self) -> int:
        return len(self.chronological_sessions)
        
    def append(self, session: Session):
        if self.chronological_sessions and session.start_ts_ms < self.chronological_sessions[-1].end_ts_ms:
            raise ValueError("Sessions must be added in chronological order and must not overlap.")
        
        self.chronological_sessions.append(session)
        
    @property
    def oldest(self) -> Session | None:
        return self.chronological_sessions[0] if self.chronological_sessions else None

    @property
    def latest(self) -> Session | None:
        return self.chronological_sessions[-1] if self.chronological_sessions else None
    
    @property
    def time_range(self) -> tuple[datetime, datetime] | None:
        if not self.chronological_sessions:
            return None
        
        oldest = self.chronological_sessions[0]
        latest = self.chronological_sessions[-1]
        return (oldest.start_datetime, latest.end_datetime)
    
    @property
    def is_empty(self) -> bool:
        return not self.chronological_sessions