from src.chronica.domain.models.app_usage_report import AppUsageReport
from src.chronica.domain.models.session_history import SessionHistory
from dataclasses import dataclass

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