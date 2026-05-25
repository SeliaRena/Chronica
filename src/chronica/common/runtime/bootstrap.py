from src.chronica.ui.presentation.settings import SessionTimelineSettings
from src.chronica.ui.resources import AppIconProvider
from src.chronica.storage.context import StorageContext
from src.chronica.storage.bootstrap import build_sqlite_storage_context
from src.chronica.common.timestamp import TimestampContextProvider
from src.chronica.common.runtime.app_runtime_context import AppRuntimeContext

def build_app_runtime_context() -> AppRuntimeContext:
    ts_ctx_provider = TimestampContextProvider()
    storage = build_sqlite_storage_context(ts_ctx_provider)
    app_icon_provider = AppIconProvider()
    session_timeline_settings = SessionTimelineSettings()
    
    return AppRuntimeContext(
        storage=storage,
        ts_ctx_provider=ts_ctx_provider,
        app_icon_provider=app_icon_provider,
        session_timeline_settings=session_timeline_settings
    )