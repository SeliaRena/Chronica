from __future__ import annotations
from dataclasses import dataclass
from src.chronica.domain.chronosystem import ChronoScale, ChronoSpan

@dataclass(slots=True, frozen=True)
class Session:
    seq: int
    start_ts_ms: int
    end_ts_ms: int
    app_name: str
    app_path: str
    window_title: str
    
    @property
    def duration(self) -> int:
        return max(0, self.end_ts_ms - self.start_ts_ms)
    
    @property
    def duration_chronospan(self) -> ChronoSpan:
        return ChronoSpan(self.duration, ChronoScale.MILLISECOND)
    
    def is_contiguous_with(self, other: Session) -> bool:
        """
        Returns true if the two sessions are contiguous \n
        ### Definition of contiguous: \n
        - The start timestamp of one session is equal to the end timestamp of the other session \n
        - The end timestamp of one session is equal to the start timestamp of the other session \n\n
        
        For example (code below is pseudocode): \n
        >>> a = Session(start_ts_ms=1, end_ts_ms=2) \n
        >>> b = Session(start_ts_ms=2, end_ts_ms=3) \n
        >>> a.is_contiguous_with(b) == True # and vice versa
        """
        
        return self.end_ts_ms == other.start_ts_ms or self.start_ts_ms == other.end_ts_ms

    def to_debug_dict(self) -> dict:
        return {
            "seq": self.seq,
            "start_ts_ms": self.start_ts_ms,
            "end_ts_ms": self.end_ts_ms,
            "app_name": self.app_name,
            "app_path": self.app_path,
            "window_title": self.window_title,
            "duration": self.duration
        }

    def to_debug_line(self) -> str:
        return f"(seq: {self.seq}, use_period: |{self.start_ts_ms} ~ {self.end_ts_ms}|, app: {self.app_name}, window: {self.window_title}, duration: {self.duration})"