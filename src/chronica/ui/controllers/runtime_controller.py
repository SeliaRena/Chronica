from __future__ import annotations

from PySide6.QtCore import QTimer

from src.chronica.application.engine.clockheart_engine import ClockheartEngine
from src.chronica.ui.presentation.models import TrackingRecordDisplay, DashboardSnapshot
from src.chronica.ui.presentation.interpreters.engine_result_interpreter import EngineResultInterpreter
from src.chronica.ui.pages.main_window import ChronicaMainWindow
from src.chronica.characters.character import Character
from src.chronica.characters.builders import DialogueRenderContextBuilder
from src.chronica.characters.dialogues import Scenario

class RuntimeController:
    def __init__(self, window: ChronicaMainWindow, engine: ClockheartEngine):
        self.window = window
        self.engine = engine
        self.app_ctx = self.window.app_ctx
        self.interpreter = EngineResultInterpreter(self.app_ctx.ts_ctx_provider)
        
        self.timer = QTimer()
        self.timer.setInterval(self.engine.tick_interval)
        self.timer.timeout.connect(self.timer_event)
        
        self.window.control_bar.set_active_nav("dashboard")
        self.window.control_bar.set_tracking_idle()
        self._connect_ui()
        
        # Chronica is alive !! :D
        dialogue_box = self.window.dialogue.text_label
        self.chronica: Character = Character(dialogue_box)
        
        # Dependency injections
        # This is a temporarily solution to let chronica gain control of every record item in tracking record list.
        # It needs a more stable solution in the future.
        self.window.tracking_archive.tracking_record_selector.set_character(self.chronica)
        
        # Connections
        dialogue_panel = self.window.dialogue
        self.chronica.finished_speaking.connect(dialogue_panel.on_dialogue_ended)
        self.chronica.next_line_confirmation_requested.connect(dialogue_panel.on_next_line_confirmation_requested)
        self.chronica.line_skippable.connect(dialogue_panel.on_line_skippable)
        
        # Say something, Chronica
        self.chronica.say_random(Scenario.BOOTUP)
        
    def _connect_ui(self) -> None:
        bar = self.window.control_bar
        bar.start_requested.connect(self.start_tracking)
        bar.stop_requested.connect(self.stop_tracking)

    def start_tracking(self) -> None:
        self.engine.start()
        self.timer.start()
        
        self.chronica.say_random(Scenario.START_TRACKING)

        self.window.control_bar.set_tracking_running()
        self.window.control_bar.set_status_hint("Tracking is active.")

        self.refresh_ui()

    def stop_tracking(self) -> None:
        self.engine.stop()
        self.timer.stop()
        
        self.chronica.say_random(Scenario.STOP_TRACKING)

        self.window.control_bar.set_tracking_idle()
        self.window.control_bar.set_status_hint("Tracking stopped.")

        ts_ctx = self.app_ctx.ts_ctx_provider.get()
        record = self.engine.generate_tracking_record()
        record_service = self.app_ctx.storage.tracking_records
        record_selector = self.window.tracking_archive.tracking_record_selector

        record_service.save(record)
        record_selector.add_tracking_record_item(TrackingRecordDisplay.from_tracking_record(record, ts_ctx))

        self.refresh_ui()
        self.engine.reset()

    def refresh_ui(self) -> None:
        snapshot: DashboardSnapshot = self.interpreter.to_dashboard_snapshot(self.engine.snapshot)
        dashboard = self.window.dashboard

        dashboard.set_current_app(snapshot.current_app)
        dashboard.set_current_window(snapshot.current_window)
        dashboard.set_last_external_app(snapshot.last_app)
        dashboard.set_last_external_window(snapshot.last_window)
        dashboard.set_last_observed_duration(snapshot.last_observed_duration)
        dashboard.set_last_observed_at(snapshot.last_app_switch_at)
        dashboard.set_tracked_time(snapshot.tracked_time)
        dashboard.set_sessions_emitted(str(snapshot.sessions_emitted))
        dashboard.set_unique_apps(str(snapshot.unique_apps_observed))
        dashboard.refresh_recent_sessions(snapshot.recent_sessions)
        
        top_apps = snapshot.top_apps
        dashboard.set_top_app(top_apps[0].app_name if len(top_apps) > 0 else "N/A")
        dashboard.refresh_top_apps(top_apps)

    def timer_event(self) -> None:
        self.engine.tick()
        self.refresh_ui()