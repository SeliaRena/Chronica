from __future__ import annotations
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from dataclasses import dataclass
from tzlocal import get_localzone_name

type UnixTimestampMs = int

def now_ts_ms() -> UnixTimestampMs:
    """
    Returns the current unix timestamp in milliseconds
    """

    return int(time.time_ns() // 1_000_000)

@dataclass(frozen=True, slots=True)
class TimestampContext:
    timezone: ZoneInfo
    
    @classmethod
    def from_local_timezone(cls) -> TimestampContext:
        return cls(ZoneInfo(get_localzone_name()))
    
    def now_datetime(self) -> datetime:
        return datetime.now(self.timezone)
    
    def datetime_from_ts_ms(self, ts_ms: UnixTimestampMs) -> datetime:
        return datetime.fromtimestamp(ts_ms / 1000, self.timezone)
    
    def ts_ms_from_datetime(self, dt: datetime) -> UnixTimestampMs:
        if dt.tzinfo is None:
            dt = dt.astimezone(self.timezone)

        return int(dt.timestamp() * 1000)
    
class TimestampContextProvider:
    def __init__(self, ts_ctx: TimestampContext | None = None) -> None:
        self._ts_ctx = ts_ctx or TimestampContext.from_local_timezone()
        
    def get(self):
        return self._ts_ctx
    
    def set(self, ts_ctx: TimestampContext):
        self._ts_ctx = ts_ctx