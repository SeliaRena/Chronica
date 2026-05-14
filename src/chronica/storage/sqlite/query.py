from dataclasses import dataclass
from enum import Enum, auto

class TrackingRecordTimeFilter(Enum):
    ALL = auto()
    TODAY = auto()
    LAST_24_HOURS = auto()
    LAST_7_DAYS = auto()
    LAST_30_DAYS = auto()

class TrackingRecordDurationFilter(Enum):
    ALL = auto()
    LESS_THAN_5_MINUTES = auto()
    LESS_THAN_1_HOUR = auto()
    LESS_THAN_HALF_DAY = auto()
    LESS_THAN_1_DAY = auto()
    MORE_OR_EQUAL_THAN_1_DAY = auto()
    
class TrackingRecordSortMode(Enum):
    NEWEST_FIRST = auto()
    OLDEST_FIRST = auto()
    LONGEST_DURATION_FIRST = auto()
    SHORTEST_DURATION_FIRST = auto()
    TITLE_ASC = auto()
    TITLE_DESC = auto()
    
@dataclass(frozen=True, slots=True)
class TrackingRecordQuery:
    search_text: str
    time_filter: TrackingRecordTimeFilter
    duration_filter: TrackingRecordDurationFilter
    sort_mode: TrackingRecordSortMode