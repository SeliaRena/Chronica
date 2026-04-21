from src.chronica.core.foreground_context_sampler import ForegroundContextSampler, SamplerResultStatus, SamplerResult
from src.chronica.core.sample_stream_sessionizer import SampleStreamSessionizer, SessionizerEvent, SessionizerResultStatus
from src.chronica.domain.app_usage_report import AppUsageReport
from src.chronica.domain.app_usage_info import AppUsageInfo
from src.chronica.domain.session_history import SessionHistory
from src.chronica.domain.chronosystem import CascadedChronoSpan, CascadingType
from src.chronica.domain.session import Session
from src.chronica.common.formatters import DIGITAL_CLOCK
from src.chronica.utils.json_util import to_pretty_json
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class TickIntervalOption:
    MS_500 = 500
    MS_1000 = 1000

@dataclass(frozen=True)
class UISnapshot:
    tracked_time: int
    current_app: str
    current_window: str
    last_app: str
    last_window: str
    last_observed_duration: int
    last_app_switch_at: datetime
    sessions_emitted: int
    unique_apps_observed: int
    top_apps: tuple[tuple[str, AppUsageInfo], ...]
    recent_sessions: tuple[Session, ...]

class ClockheartEngine:
    def __init__(self, tick_interval: int = TickIntervalOption.MS_1000):
        self._ticking = False
        self._sampler = ForegroundContextSampler()
        self._sessionizer = SampleStreamSessionizer()
        self.tick_interval = tick_interval
        self.ideal_passed_time_ms = 0
        self.report = AppUsageReport()
        self.history = SessionHistory()
    
    @property
    def current_cycle_duration(self) -> str:
        duration = self.history.latest.end_ts_ms - self.history.oldest.start_ts_ms
        return DIGITAL_CLOCK[CascadedChronoSpan.from_total_ms(duration).transform(CascadingType.FULL_PADDED)]
    
    @property
    def ui_snapshot(self) -> UISnapshot:
        return UISnapshot(
            tracked_time=self.ideal_passed_time_ms,
            current_app=self._sampler.latest_sample.exe_name,
            current_window=self._sampler.latest_sample.normalized_window_title,
            last_app=self.history.latest.app_name if not self.history.is_empty else "N/A",
            last_window=self.history.latest.window_title if not self.history.is_empty else "N/A",
            last_observed_duration=self.history.latest.duration if not self.history.is_empty else 0,
            last_app_switch_at=self.history.latest.end_datetime if not self.history.is_empty else datetime.min,
            sessions_emitted=len(self.history),
            unique_apps_observed=len(self.report.app_usage_map),
            top_apps=tuple(sorted(self.report.app_usage_map.items(), key=lambda app: app[1].total_usage_time_ms, reverse=True)[:5]),
            recent_sessions=tuple(self.history.chronological_sessions[-5:] if len(self.history) >= 5 else self.history.chronological_sessions)
        )

    @property
    def debug_dump(self) -> str:
        return to_pretty_json({
            "App usage report of this cycle": self.report.to_debug_dict(),
            "Full session history of this cycle": self.history.to_debug_list()
        })
        
    def _try_log_sampler_external_error(self, sampler_result: SamplerResult):
        if sampler_result.status == SamplerResultStatus.EXTERNAL_ERROR:
            logger.error("External error occurred: %s", sampler_result.error_class)

    def start(self):
        logger.info("Starting Clockheart Engine")
        self.ideal_passed_time_ms = 0
        
        sampler_result = self._sampler.start_sampling()
        if sampler_result.status != SamplerResultStatus.SUCCESS:
            logger.error("Failed to start sampler, returned status: [%s], message: %s", sampler_result.status.name, sampler_result.message)
            self._try_log_sampler_external_error(sampler_result)
        else:
            logger.info("Sampler started successfully, emitted event: %s", sampler_result.event.name)
        logger.debug("Initial Sampler result: %s", to_pretty_json(sampler_result.to_debug_dict()))
        
        sessionizer_result = self._sessionizer.consume(sampler_result)
        if sessionizer_result.status == SessionizerResultStatus.OP_FAILED:
            logger.error("Sessionizer failed during initial consume: %s", sessionizer_result.message)
            logger.error("Events emitted during failure: %s", [event.name for event in sessionizer_result.events])
            logger.error("Error type: %s", sessionizer_result.error_type.name)
        else:
            logger.info("Sessionizer initialized successfully, emitted events: %s", [event.name for event in sessionizer_result.events])
        logger.debug("Initial Sessionizer result: %s", to_pretty_json(sessionizer_result.to_debug_dict()))
        
    def stop(self):
        self._ticking = False
        logger.info("Stopping Clockheart Engine, ticking phase ended")

        sampler_result = self._sampler.stop_sampling()
        if sampler_result.status != SamplerResultStatus.SUCCESS:
            logger.error("Failed to stop sampler, returned status: [%s], message: %s", sampler_result.status.name, sampler_result.message)
            self._try_log_sampler_external_error(sampler_result)
        else:
            logger.info("Sampler stopped successfully, emitted event: %s", sampler_result.event.name)
        logger.debug("Terminal Sampler result: %s", to_pretty_json(sampler_result.to_debug_dict()))
        
        sessionizer_result = self._sessionizer.consume(sampler_result)
        if sessionizer_result.status == SessionizerResultStatus.OP_FAILED:
            logger.error("Sessionizer failed during terminal consume: %s", sessionizer_result.message)
            logger.error("Events emitted during failure: %s", [event.name for event in sessionizer_result.events])
            logger.error("Error type: %s", sessionizer_result.error_type.name)
        elif SessionizerEvent.SESSION_EMITTED in sessionizer_result.events:
            logger.info("Sessionizer processed terminal sampler result successfully, emitted events: %s", [event.name for event in sessionizer_result.events])
            self.report.add_session(sessionizer_result.session)
            self.history.append(sessionizer_result.session)
        logger.debug("Terminal Sessionizer result: %s", to_pretty_json(sessionizer_result.to_debug_dict()))
        
        logger.info("This cycle's duration: %s", self.current_cycle_duration)
        
    def tick(self):
        if not self._ticking:
            self._ticking = True
            logger.info("Clockheart Engine ticking phase started")
        self.ideal_passed_time_ms += self.tick_interval
        
        sampler_result = self._sampler.on_tick()
        if sampler_result.status != SamplerResultStatus.SUCCESS:
            logger.error("Sampler tick failed, returned status: [%s], message: %s", sampler_result.status.name, sampler_result.message)
            self._try_log_sampler_external_error(sampler_result)

        sessionizer_result = self._sessionizer.consume(sampler_result)
        if SessionizerEvent.SESSION_EMITTED in sessionizer_result.events and sessionizer_result.status == SessionizerResultStatus.OP_SUCCESS:
            logger.info("New session emitted during tick, adding to report and history")
            self.report.add_session(sessionizer_result.session)
            self.history.append(sessionizer_result.session)
        elif sessionizer_result.status == SessionizerResultStatus.OP_FAILED:
            logger.error("Sessionizer failed during tick consume: %s", sessionizer_result.message)
            logger.error("Events emitted during failure: %s", [event.name for event in sessionizer_result.events])
            logger.error("Error type: %s", sessionizer_result.error_type.name)
        elif sessionizer_result.status == SessionizerResultStatus.OP_IGNORED:
            logger.debug("Same windows, no action taken.")
            
        if sessionizer_result.status != SessionizerResultStatus.OP_IGNORED:
            logger.debug("Engine.tick Sessionizer result: %s", to_pretty_json(sessionizer_result.to_debug_dict()))
            logger.debug("Engine.tick Sampler result: %s", to_pretty_json(sampler_result.to_debug_dict()))