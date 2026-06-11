from src.chronica.storage.sqlite.repositories import TrackingRecordRepository

from src.chronica.storage.sqlite.query import (
    TrackingRecordTimeFilter,
    TrackingRecordDurationFilter,
    TrackingRecordSortMode,
    TrackingRecordQuery
)

from src.chronica.domain.chronosystem import ChronoSpan, ChronoScale
from src.chronica.domain.models import (
    TrackingRecord
)

from src.chronica.common.timestamp import TimestampContextProvider
from src.chronica.common.timerange import (
    TimestampMsRange,
    DatetimeRange,
    DatetimeRangeMaker
)

import datetime

class TrackingRecordService:
    def __init__(self, repo: TrackingRecordRepository, ts_ctx_provider: TimestampContextProvider) -> None:
        self._repo = repo
        self._ts_ctx_provider = ts_ctx_provider

    def save(self, record: TrackingRecord) -> int:
        return self._repo.save(record)

    def get_by_query(self, query: TrackingRecordQuery) -> list[TrackingRecord]:
        res: list[TrackingRecord] = []
        
        time_filter = query.time_filter
        duration_filter = query.duration_filter
        search_text = query.search_text
        sort_mode = query.sort_mode
        now = self._ts_ctx_provider.get().now_datetime()
        
        match time_filter:
            case TrackingRecordTimeFilter.ALL:
                res = self._repo.get_all()
            case TrackingRecordTimeFilter.TODAY:
                ts_ms_range = DatetimeRangeMaker(now).since_days_ago_start(0).as_ts_ms_range()
                res = self._repo.get_by_ts_ms_range(ts_ms_range.start, ts_ms_range.end)
            case TrackingRecordTimeFilter.LAST_24_HOURS:
                ts_ms_range = DatetimeRangeMaker(now).hours_till_now(24).as_ts_ms_range()
                res = self._repo.get_by_ts_ms_range(ts_ms_range.start, ts_ms_range.end)
            case TrackingRecordTimeFilter.LAST_7_DAYS:
                ts_ms_range = DatetimeRangeMaker(now).since_days_ago_start(7).as_ts_ms_range()
                res = self._repo.get_by_ts_ms_range(ts_ms_range.start, ts_ms_range.end)
            case TrackingRecordTimeFilter.LAST_30_DAYS:
                ts_ms_range = DatetimeRangeMaker(now).since_days_ago_start(30).as_ts_ms_range()
                res = self._repo.get_by_ts_ms_range(ts_ms_range.start, ts_ms_range.end)
            case _:
                # fallback to ALL
                res = self._repo.get_all()
                
        match duration_filter:
            case TrackingRecordDurationFilter.ALL:
                pass
            case TrackingRecordDurationFilter.LESS_THAN_5_MINUTES:
                res = [r for r in res if r.duration < ChronoSpan(5, ChronoScale.MINUTE).in_ms]
            case TrackingRecordDurationFilter.LESS_THAN_1_HOUR:
                res = [r for r in res if r.duration < ChronoSpan(1, ChronoScale.HOUR).in_ms]
            case TrackingRecordDurationFilter.LESS_THAN_HALF_DAY:
                res = [r for r in res if r.duration < ChronoSpan(12, ChronoScale.HOUR).in_ms]
            case TrackingRecordDurationFilter.LESS_THAN_1_DAY:
                res = [r for r in res if r.duration < ChronoSpan(1, ChronoScale.DAY).in_ms]
            case TrackingRecordDurationFilter.MORE_OR_EQUAL_THAN_1_DAY:
                res = [r for r in res if r.duration >= ChronoSpan(1, ChronoScale.DAY).in_ms]
            case _:
                # fallback to ALL
                pass
            
        if search_text is not None and search_text != "":
            res = [r for r in res if search_text.casefold() in r.title.casefold()]
        
        match sort_mode:
            case TrackingRecordSortMode.NEWEST_FIRST:
                res.sort(key=lambda r: r.generated_at_ts_ms, reverse=True)
            case TrackingRecordSortMode.OLDEST_FIRST:
                res.sort(key=lambda r: r.generated_at_ts_ms)
            case TrackingRecordSortMode.LONGEST_DURATION_FIRST:
                res.sort(key=lambda r: r.duration, reverse=True)
            case TrackingRecordSortMode.SHORTEST_DURATION_FIRST:
                res.sort(key=lambda r: r.duration)
            case TrackingRecordSortMode.TITLE_ASC:
                res.sort(key=lambda r: r.title)
            case TrackingRecordSortMode.TITLE_DESC:
                res.sort(key=lambda r: r.title, reverse=True)
            case _:
                # fallback to TITLE_ASC
                res.sort(key=lambda r: r.title)
        
        return res

    def delete_by_title(self, record_title: str) -> None:
        self._repo.delete_by_title(record_title)