from src.chronica.ui.presentation.models import (
    SessionDisplay,
    AppUsageInfoDisplay,
    DashboardSnapshot
)
from src.chronica.ui.presentation.formatters import simplistic_simplified_ms, ymd_hms
from src.chronica.application.engine.clockheart_engine import EngineSnapshot
from src.chronica.common.timestamp import TimestampContextProvider

class EngineResultInterpreter:
    def __init__(self, ts_ctx_provider: TimestampContextProvider):
        self.ts_ctx_provider = ts_ctx_provider

    def to_dashboard_snapshot(self, engine_snapshot: EngineSnapshot) -> DashboardSnapshot:
        ts_ctx = self.ts_ctx_provider.get()
        
        return DashboardSnapshot(
            tracked_time=simplistic_simplified_ms(engine_snapshot.ideal_elapsed_time_ms),
            current_app=engine_snapshot.current_app,
            current_window=engine_snapshot.current_window,
            last_app=engine_snapshot.last_app,
            last_window=engine_snapshot.last_window,
            last_observed_duration=simplistic_simplified_ms(engine_snapshot.last_observed_duration),
            last_app_switch_at=ymd_hms(ts_ctx.datetime_from_ts_ms(engine_snapshot.last_app_switch_at_ts_ms)),
            sessions_emitted=engine_snapshot.sessions_emitted,
            unique_apps_observed=engine_snapshot.unique_apps_observed,
            top_apps=tuple((app_name, AppUsageInfoDisplay.from_app_usage_info(app_usage_info)) for app_name, app_usage_info in engine_snapshot.top_apps),
            recent_sessions=tuple(SessionDisplay.from_session(session, ts_ctx) for session in engine_snapshot.recent_sessions)
        )