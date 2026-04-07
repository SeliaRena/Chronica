from session import Session
from app_usage_info import AppUsageInfo

class AppUsageReport:
    def __init__(self, app_usage_map: dict[str, AppUsageInfo] | None = None,
                 total_usage_time_ms: int = 0):
        self.app_usage_map: dict[str, AppUsageInfo] = app_usage_map if app_usage_map is not None else {}
        self.total_usage_time_ms: int = total_usage_time_ms
    
    def add_session(self, session: Session) -> None:
        if session.app_name not in self.app_usage_map:
            self.app_usage_map[session.app_name] = AppUsageInfo(session.app_name)
        
        self.app_usage_map[session.app_name].add_session(session)
        self.total_usage_time_ms += session.duration