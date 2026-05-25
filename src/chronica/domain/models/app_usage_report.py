from src.chronica.domain.models.session import Session
from src.chronica.domain.models.app_usage_info import AppUsageInfo

class AppUsageReport:
    def __init__(self, app_usage_map: dict[str, AppUsageInfo] | None = None,
                 total_usage_time_ms: int = 0):
        self.app_usage_map: dict[str, AppUsageInfo] = app_usage_map if app_usage_map is not None else {}
        self.total_usage_time_ms: int = total_usage_time_ms
    
    def add_session(self, session: Session) -> None:
        if session.app_name not in self.app_usage_map:
            self.app_usage_map[session.app_name] = AppUsageInfo(session.app_name, session.app_path)
        
        self.app_usage_map[session.app_name].add_session(session)
        self.total_usage_time_ms += session.duration

    @property
    def app_count(self) -> int:
        return len(self.app_usage_map)

    @property
    def total_app_entry_count(self) -> int:
        return sum(a.app_entry_count for a in self.app_usage_map.values())

    def to_debug_dict(self) -> dict:
        return {
            "total_usage_time_ms": self.total_usage_time_ms,
            "app_usage_map": {app_name: info.to_debug_dict() for app_name, info in self.app_usage_map.items()}
        }