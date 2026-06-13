from dataclasses import dataclass
from datetime import datetime, timedelta, time
from src.chronica.common.timestamp import UnixTimestampMs, as_ts_ms

@dataclass(frozen=True, slots=True)
class TimestampMsRange:
    start: UnixTimestampMs
    end: UnixTimestampMs
    
    def __post_init__(self) -> None:
        if self.start > self.end:
            raise ValueError(f"Invalid timestamp range: {self.start!r} > {self.end!r}")
    
    def __contains__(self, ts_ms: UnixTimestampMs) -> bool:
        return self.start <= ts_ms <= self.end
    
    @property
    def duration(self) -> int:
        return max(0, self.end - self.start)
    
@dataclass(frozen=True, slots=True)
class DatetimeRange:
    start: datetime
    end: datetime
    
    def __post_init__(self) -> None:
        if not (self.start.tzinfo and self.end.tzinfo and self.start.tzinfo == self.end.tzinfo):
            raise ValueError(f"Inconsistent timezone: {self.start.tzinfo!r} != {self.end.tzinfo!r}")
        if self.start > self.end:
            raise ValueError(f"Invalid datetime range: {self.start!r} > {self.end!r}")
    
    def __contains__(self, dt: datetime) -> bool:
        if dt.tzinfo != self.start.tzinfo or dt.tzinfo != self.end.tzinfo:
            raise ValueError(f"Inconsistent timezone: {dt.tzinfo!r} != (start & end: {self.start.tzinfo!r})")
        return self.start <= dt <= self.end
    
    def as_ts_ms_range(self) -> TimestampMsRange:
        return TimestampMsRange(as_ts_ms(self.start), as_ts_ms(self.end))

@dataclass(frozen=True, slots=True)
class DatetimeRangeMaker:
    timepoint: datetime
    
    @staticmethod
    def _start_of_day(dt: datetime) -> datetime:
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)
    
    def since_days_ago_start(self, days: int) -> DatetimeRange:
        return DatetimeRange(self._start_of_day(self.timepoint - timedelta(days=days)), self.timepoint)
    
    def hours_till_now(self, hours: int) -> DatetimeRange:
        return DatetimeRange(self.timepoint - timedelta(hours=hours), self.timepoint)
    
    def minutes_till_now(self, minutes: int) -> DatetimeRange:
        return DatetimeRange(self.timepoint - timedelta(minutes=minutes), self.timepoint)

def strip_to_hms(dt: datetime) -> time:
    return dt.time().replace(microsecond=0)

@dataclass(frozen=True, slots=True)
class HmsRange:
    start: time
    end: time
    
    def __post_init__(self) -> None:
        if self.start.microsecond != 0 or self.end.microsecond != 0:
            raise ValueError(f"Microsecond must be stripped: {self.start!r} & {self.end!r}")
    
    def __contains__(self, t: time) -> bool:
        if self.start <= self.end:
            return self.start <= t <= self.end
        else:
            return self.start <= t or t <= self.end