from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class RecentSessionsItemData:
    start_time: str
    end_time: str
    duration: str
    app_name: str
    app_path: str
    window_title: str
    is_first: bool = False
    is_cross_day: bool = False