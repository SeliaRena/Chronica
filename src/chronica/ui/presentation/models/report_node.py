from __future__ import annotations
from src.chronica.ui.presentation.formatters import simplistic_simplified_ms, ymd_hms
from src.chronica.common.timestamp import TimestampContextProvider
from dataclasses import dataclass, field

from src.chronica.domain.models import (
    SessionHistory,
    WindowUsageInfo,
    AppUsageInfo,
    AppUsageReport
)

@dataclass(frozen=True, slots=True)
class ReportNode:
    name: str
    duration: str = ""
    detail: str = ""
    tooltip: str = ""
    default_expanded: bool = False
    children: tuple[ReportNode, ...] = field(default_factory=tuple)
    
class ReportNodeMapper:
    def __init__(self, ts_ctx_provider: TimestampContextProvider) -> None:
        self.ts_ctx_provider = ts_ctx_provider

    def _from_session_history(self, session_history: SessionHistory) -> tuple[ReportNode, ...]:
        ts_ctx = self.ts_ctx_provider.get()
        return (
            ReportNode(name="first seen", detail=ymd_hms(ts_ctx.datetime_from_ts_ms(session_history.oldest.start_ts_ms))),
            ReportNode(name="last seen", detail=ymd_hms(ts_ctx.datetime_from_ts_ms(session_history.latest.end_ts_ms))),
        )

    def _from_window_usage_info(self, window_usage_info: WindowUsageInfo) -> ReportNode:
        return ReportNode(
            name=window_usage_info.window_title,
            duration=simplistic_simplified_ms(window_usage_info.total_usage_time_ms),
            detail=f"focus count: {window_usage_info.session_count} time(s)",
            children=self._from_session_history(window_usage_info.session_history)
        )

    def from_app_usage_report(self, app_usage_report: AppUsageReport) -> ReportNode:
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
                        self._from_window_usage_info(window_usage_info) for window_usage_info in app_usage_info.window_usage_map.values()
                    )
                ) for app_usage_info in app_usage_report.app_usage_map.values())
            ),)
        )