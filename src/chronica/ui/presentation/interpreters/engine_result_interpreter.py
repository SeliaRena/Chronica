from src.chronica.domain.models import (
    AppUsageInfo,
    AppUsageReport,
    SessionHistory
)

from src.chronica.ui.presentation.models import (
    SessionDisplay,
    AppUsageInfoDisplay,
    DashboardSnapshot,
    TopAppsItemData
)

from src.chronica.ui.presentation.formatters import simplistic_simplified_ms, ymd_hms
from src.chronica.application.engine.clockheart_engine import EngineSnapshot
from src.chronica.common.timestamp import TimestampContextProvider

class EngineResultInterpreter:
    def __init__(self, ts_ctx_provider: TimestampContextProvider):
        self.ts_ctx_provider = ts_ctx_provider
    
    def _extract_top_apps(self, report: AppUsageReport) -> tuple[TopAppsItemData, ...]:
        top_apps_raw = sorted(
            report.app_usage_map.values(), 
            key=lambda appinfo: appinfo.total_usage_time_ms, 
            reverse=True
        )[:5]
        
        return tuple(
            TopAppsItemData(
                app_name=appinfo.app_name,
                bar_ratio=(
                    appinfo.total_usage_time_ms / top_apps_raw[0].total_usage_time_ms
                    if top_apps_raw and top_apps_raw[0].total_usage_time_ms > 0 else 0.0
                ),
                share_ratio=(
                    appinfo.total_usage_time_ms / report.total_usage_time_ms
                    if report.total_usage_time_ms > 0 else 0.0
                ),
                duration=simplistic_simplified_ms(appinfo.total_usage_time_ms)
            ) for appinfo in top_apps_raw
        )
    
    def _extract_recent_sessions(self, history: SessionHistory) -> tuple[SessionDisplay, ...]:
        return tuple(
            SessionDisplay.from_session(session, self.ts_ctx_provider.get()) 
            for session in history.chronological_sessions[-5:]
        )

    def to_dashboard_snapshot(self, engine_snapshot: EngineSnapshot) -> DashboardSnapshot:
        ts_ctx = self.ts_ctx_provider.get()
        report = engine_snapshot.app_usage_report
        history = engine_snapshot.session_history
        
        last_app = history.latest.app_name if history.latest else "N/A"
        last_window = history.latest.window_title if history.latest else "N/A"
        last_observed_duration = simplistic_simplified_ms(history.latest.duration) if history.latest else "N/A"
        last_app_switch_at = ymd_hms(ts_ctx.datetime_from_ts_ms(history.latest.end_ts_ms)) if history.latest else "N/A"
        sessions_emitted = len(history)
        unique_apps_observed = len(report.app_usage_map.keys())
        
        return DashboardSnapshot(
            tracked_time=simplistic_simplified_ms(engine_snapshot.ideal_elapsed_time_ms),
            current_app=engine_snapshot.current_app,
            current_window=engine_snapshot.current_window,
            last_app=last_app,
            last_window=last_window,
            last_observed_duration=last_observed_duration,
            last_app_switch_at=last_app_switch_at,
            sessions_emitted=sessions_emitted,
            unique_apps_observed=unique_apps_observed,
            top_apps=self._extract_top_apps(report),
            recent_sessions=self._extract_recent_sessions(history)
        )