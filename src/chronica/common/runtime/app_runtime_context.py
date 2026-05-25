from src.chronica.common.timestamp import TimestampContextProvider
from src.chronica.storage.context import StorageContext
from src.chronica.ui.presentation.settings import SessionTimelineSettings
from src.chronica.ui.resources import AppIconProvider
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class AppRuntimeContext:
    storage: StorageContext
    ts_ctx_provider: TimestampContextProvider
    app_icon_provider: AppIconProvider
    session_timeline_settings: SessionTimelineSettings