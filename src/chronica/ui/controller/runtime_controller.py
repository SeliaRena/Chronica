from __future__ import annotations

from PySide6.QtCore import QTimer

from src.chronica.application.engine.clockheart_engine import ClockheartEngine
from src.chronica.common.formatters import SIMPLISTIC
from src.chronica.domain.chronosystem import CascadedChronoSpan
from src.chronica.ui.main_window import ChronicaMainWindow

class RuntimeController:
    def __init__(self, window: ChronicaMainWindow, engine: ClockheartEngine):
        self.window = window
        self.engine = engine
        
        self.timer = QTimer()
        self.timer.setInterval(self.engine.tick_interval)
        self.timer.timeout.connect(self.timer_event)
        
        self.window.control_bar.set_active_nav("dashboard")
        self.window.control_bar.set_tracking_idle()
        self._connect_ui()
        
    def _connect_ui(self) -> None:
        bar = self.window.control_bar
        bar.start_requested.connect(self.start_tracking)
        bar.stop_requested.connect(self.stop_tracking)

    def start_tracking(self) -> None:
        self.engine.start()
        self.timer.start()

        self.window.control_bar.set_tracking_running()
        self.window.control_bar.set_status_hint("Tracking is active.")

        self.refresh_ui()

    def stop_tracking(self) -> None:
        self.engine.stop()
        self.timer.stop()

        self.window.control_bar.set_tracking_idle()
        self.window.control_bar.set_status_hint("Tracking stopped.")

        self.refresh_ui()
        
    def _ui_format_time(self, total_ms: int) -> str:
        return SIMPLISTIC[CascadedChronoSpan.from_total_ms(total_ms)] if total_ms >= 1000 else "<1s"

    def refresh_ui(self) -> None:
        snapshot = self.engine.ui_snapshot
        dashboard = self.window.dashboard

        dashboard.set_current_app(snapshot.current_app)
        dashboard.set_current_window(snapshot.current_window)
        dashboard.set_last_external_app(snapshot.last_app)
        dashboard.set_last_external_window(snapshot.last_window)
        dashboard.set_last_observed_duration(self._ui_format_time(snapshot.last_observed_duration))
        dashboard.set_last_observed_at(snapshot.last_app_switch_at.isoformat())
        dashboard.set_tracked_time(self._ui_format_time(snapshot.tracked_time))
        dashboard.set_sessions_emitted(str(snapshot.sessions_emitted))
        dashboard.set_unique_apps(str(snapshot.unique_apps_observed))
        dashboard.refresh_recent_sessions(snapshot.recent_sessions)
        
        top_apps = snapshot.top_apps
        dashboard.set_top_app(top_apps[0][0] if len(top_apps) > 0 else "N/A")

    def timer_event(self) -> None:
        self.engine.tick()
        self.refresh_ui()