from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from src.chronica.domain.chronosystem import ChronoScale, ChronoSpan, CascadedChronoSpan
from src.chronica.common.formatters import HUMAN_READABLE
import json

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
    
    def to_debug_dict(self) -> dict:
        return {
            "id": self.id,
            "start_ts_ms": self.start_datetime,
            "end_ts_ms": self.end_datetime,
            "app_name": self.app_name,
            "app_path": self.app_path,
            "window_title": self.window_title,
            "duration": HUMAN_READABLE[CascadedChronoSpan.from_total_ms(self.duration)]
        }

    def to_debug_line(self) -> str:
        return f"(id: {self.id}, use_period: |{self.start_datetime} ~ {self.end_datetime}|, app: {self.app_name}, window: {self.window_title}, duration: {HUMAN_READABLE[CascadedChronoSpan.from_total_ms(self.duration)]})"