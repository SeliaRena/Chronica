from src.chronica.domain.session import Session
from src.chronica.domain.app_usage_info import AppUsageInfo
from src.chronica.domain.chronosystem import CascadedChronoSpan
from src.chronica.common.formatters import HUMAN_READABLE

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
        
    def to_debug_dict(self) -> dict:
        return {
            "total_usage_time_ms": HUMAN_READABLE[CascadedChronoSpan.from_total_ms(self.total_usage_time_ms)],
            "app_usage_map": {app_name: info.to_debug_dict() for app_name, info in self.app_usage_map.items()}
        }