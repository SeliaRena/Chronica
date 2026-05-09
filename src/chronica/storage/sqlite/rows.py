from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class TrackingRecordRow:
    id: int | None
    title: str
    description: str
    generated_at_ts_ms: int
    start_ts_ms: int
    end_ts_ms: int
    created_at_ts_ms: int

@dataclass(frozen=True, slots=True)
class SessionRow:
    id: int | None
    record_id: int
    session_seq: int
    start_ts_ms: int
    end_ts_ms: int
    app_name: str
    app_path: str
    window_title: str

    @property
    def duration(self) -> int:
        return max(0, self.end_ts_ms - self.start_ts_ms)