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