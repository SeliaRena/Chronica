from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from chronosystem import ChronoScale, ChronoSpan

@dataclass(slots=True, frozen=True)
class Session:
    id: str
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
    
    @property
    def start_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.start_ts_ms / 1000)
    
    @property
    def end_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.end_ts_ms / 1000)