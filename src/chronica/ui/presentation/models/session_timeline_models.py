from src.chronica.ui.presentation.models.general_display_models import SessionDisplay
from dataclasses import dataclass
from typing import Any, Literal
from datetime import datetime

@dataclass(slots=True)
class SessionTimelineSegment:
    key: str
    row_key: str
    session: SessionDisplay
    color_key: str
    tooltip: str = ""
    color_code: str = ""
    
    def set_color_code(self, color_code: str) -> None:
        self.color_code = color_code

    def to_view_dict(self) -> dict:
        return {
            "color": self.color_code,
            "tooltip": self.tooltip,
            "session": {
                "appName": self.session.app_name,
                "windowTitle": self.session.window_title,
                "startMs": self.session.start.timestamp() * 1000,
                "endMs": self.session.end.timestamp() * 1000
            }
        }
    
@dataclass(frozen=True, slots=True)
class SessionTimelineRow:
    key: str
    label: str
    segments: tuple[SessionTimelineSegment, ...] = ()
    
    def __len__(self) -> int:
        return len(self.segments)

    def to_view_dict(self) -> dict:
        return {
            "label": self.label,
            "segments": [s.to_view_dict() for s in self.segments]
        }
    
@dataclass(frozen=True, slots=True)
class SessionTimeline:
    rows: tuple[SessionTimelineRow, ...] = ()
    
    def __len__(self) -> int:
        return len(self.rows)

    def to_view_dict(self) -> dict:
        return [r.to_view_dict() for r in self.rows]

@dataclass(frozen=True, slots=True)
class QmlSession:
    app_name: str
    app_path: str
    window_title: str
    start_ts_ms: int
    end_ts_ms: int
    start_dt_text: str
    end_dt_text: str
    duration_ms: int
    duration_text: str
    timezone_info: str
    
    def to_view_dict(self) -> dict[str, Any]:
        return {
            "appName": self.app_name,
            "appPath": self.app_path,
            "windowTitle": self.window_title,
            "startTsMs": self.start_ts_ms,
            "endTsMs": self.end_ts_ms,
            "startDtText": self.start_dt_text,
            "endDtText": self.end_dt_text,
            "durationMs": self.duration_ms,
            "durationText": self.duration_text,
            "timezoneInfo": self.timezone_info
        }

@dataclass(frozen=True, slots=True)
class QmlSegment:
    real_x: float
    real_width: float
    color: str
    session: QmlSession
    tiny: bool = False
    tooltip: str = ""
    
    def to_view_dict(self) -> dict[str, Any]:
        return {
            "realX": self.real_x,
            "realWidth": self.real_width,
            "color": self.color,
            "session": self.session.to_view_dict(),
            "tiny": self.tiny,
            "tooltip": self.tooltip
        }

@dataclass(frozen=True, slots=True)
class QmlRepeaterItem:
    kind: Literal["normal", "clustered"]
    draw_x: float
    draw_width: float
    hit_test_width: float
    segments: tuple[QmlSegment, ...] = ()
    tooltip: str = ""
    
    def to_view_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "drawX": self.draw_x,
            "drawWidth": self.draw_width,
            "hitTestWidth": self.hit_test_width,
            "segments": [s.to_view_dict() for s in self.segments],
            "tooltip": self.tooltip
        }

@dataclass(frozen=True, slots=True)
class QmlRow:
    label: str
    repeater_items: tuple[QmlRepeaterItem, ...] = ()
    
    def to_view_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "repeaterItems": [ri.to_view_dict() for ri in self.repeater_items]
        }

@dataclass(frozen=True, slots=True)
class QmlAxisTick:
    real_x: float
    timestamp_ms: int
    label: str
    kind: Literal["minor", "day_boundary"]
    
    def to_view_dict(self) -> dict[str, Any]:
        return {
            "realX": self.real_x,
            "timestampMs": self.timestamp_ms,
            "label": self.label,
            "kind": self.kind
        }

@dataclass(frozen=True, slots=True)
class QmlData:
    visible_start_ts_ms: int
    visible_end_ts_ms: int
    axis_ticks: tuple[QmlAxisTick, ...] = ()
    rows: tuple[QmlRow, ...] = ()

    def to_view_dict(self) -> dict[str, Any]:
        return {
            "visibleStartTsMs": self.visible_start_ts_ms,
            "visibleEndTsMs": self.visible_end_ts_ms,
            "axisTicks": [tick.to_view_dict() for tick in self.axis_ticks],
            "rows": [r.to_view_dict() for r in self.rows]
        }