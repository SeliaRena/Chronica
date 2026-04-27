from src.chronica.domain.app_usage_report import AppUsageReport
from src.chronica.domain.session_history import SessionHistory
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True, slots=True)
class TrackingRecord:
    title: str
    generated_at_ts_ms: int
    start_ts_ms: int
    end_ts_ms: int
    app_usage_report: AppUsageReport
    session_history: SessionHistory
    description: str = "no description"
    
    @property
    def duration(self) -> int:
        return max(0, self.end_ts_ms - self.start_ts_ms)
    
    @property
    def start_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.start_ts_ms / 1000)
    
    @property
    def end_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.end_ts_ms / 1000)
    
    @property
    def generated_at_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.generated_at_ts_ms / 1000)