from enum import Enum, auto
from dataclasses import dataclass

class SessionTimelineGroupingMode(Enum):
    BY_APP = auto()
    BY_WINDOW = auto()
    
class SessionTimelineRowSorting(Enum):
    ALPHABETICAL = auto()
    REVERSED_ALPHABETICAL = auto()
    
@dataclass(slots=True)
class SessionTimelineSettings:
    grouping_mode: SessionTimelineGroupingMode = SessionTimelineGroupingMode.BY_APP
    row_sorting: SessionTimelineRowSorting = SessionTimelineRowSorting.REVERSED_ALPHABETICAL