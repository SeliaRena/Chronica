from src.chronica.domain.session import Session

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
    def time_range_ts_ms(self) -> tuple[int, int] | None:
        """
        Returns the start and end timestamps of the oldest and latest session in the history, respectively.
        """

        if not self.chronological_sessions:
            return None
        
        oldest = self.chronological_sessions[0]
        latest = self.chronological_sessions[-1]
        return (oldest.start_ts_ms, latest.end_ts_ms)
    
    @property
    def is_empty(self) -> bool:
        return not self.chronological_sessions
    
    def to_debug_list(self) -> list[str]:
        return [session.to_debug_line() for session in self.chronological_sessions]