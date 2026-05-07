from src.chronica.common.timestamp import TimestampContextProvider
from src.chronica.ui.presentation.settings import SessionTimelineSettings
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class AppRuntimeContext:
    ts_ctx_provider: TimestampContextProvider = field(default_factory=TimestampContextProvider)
    session_timeline_settings: SessionTimelineSettings = field(default_factory=SessionTimelineSettings)