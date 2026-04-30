from __future__ import annotations
from src.chronica.domain.app_usage_report import AppUsageReport
from src.chronica.domain.app_usage_info import AppUsageInfo
from src.chronica.domain.window_usage_info import WindowUsageInfo
from src.chronica.domain.session_history import SessionHistory
from src.chronica.ui.data_display.time_format import simplistic_simplified_ms
from src.chronica.ui.data_display.datetime_format import ymd_hms
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class ReportNode:
    name: str
    duration: str = ""
    detail: str = ""
    tooltip: str = ""
    default_expanded: bool = False
    children: tuple[ReportNode, ...] = field(default_factory=tuple)

def session_history_to_report_nodes(session_history: SessionHistory) -> tuple[ReportNode, ...]:
    return (
        ReportNode(name="first seen", detail=ymd_hms(session_history.oldest.start_ts_ms)),
        ReportNode(name="last seen", detail=ymd_hms(session_history.latest.end_ts_ms)),
    )

def window_usage_info_to_report_node(window_usage_info: WindowUsageInfo) -> ReportNode:
    return ReportNode(
        name=window_usage_info.window_title,
        duration=simplistic_simplified_ms(window_usage_info.total_usage_time_ms),
        detail=f"focus count: {window_usage_info.focus_count} time(s)",
        children=session_history_to_report_nodes(window_usage_info.session_history)
    )

def app_usage_report_to_report_node(app_usage_report: AppUsageReport) -> ReportNode:
    return ReportNode(
        name="App Usage Report",
        default_expanded=True,
        children=(ReportNode(
            name="All Applications",
            duration=simplistic_simplified_ms(app_usage_report.total_usage_time_ms),
            default_expanded=True,
            children=tuple(ReportNode(
                name=app_usage_info.app_name,
                duration=simplistic_simplified_ms(app_usage_info.total_usage_time_ms),
                detail=f"path: {app_usage_info.app_path}",
                children=tuple(
                    window_usage_info_to_report_node(window_usage_info) for window_usage_info in app_usage_info.window_usage_map.values()
                )
            ) for app_usage_info in app_usage_report.app_usage_map.values())
        ),)
    )