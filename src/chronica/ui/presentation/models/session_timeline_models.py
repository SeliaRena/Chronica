from src.chronica.ui.presentation.models.general_display_models import SessionDisplay
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class SessionTimelineSegment:
    key: str
    row_key: str
    session: SessionDisplay
    color_key: str
    tooltip: str = ""
    
@dataclass(frozen=True, slots=True)
class SessionTimelineRow:
    key: str
    label: str
    segments: tuple[SessionTimelineSegment, ...] = ()
    
    def __len__(self) -> int:
        return len(self.segments)
    
@dataclass(frozen=True, slots=True)
class SessionTimeline:
    rows: tuple[SessionTimelineRow, ...] = ()
    
    def __len__(self) -> int:
        return len(self.rows)