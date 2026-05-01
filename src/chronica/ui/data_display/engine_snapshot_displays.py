from dataclasses import dataclass
from src.chronica.ui.data_display.display_models import SessionDisplay, AppUsageInfoDisplay

type ChronoDisplayOutput = str
type DatetimeDisplayOutput = str

type TopAppsDisplayEntry = tuple[str, AppUsageInfoDisplay]

@dataclass(frozen=True, slots=True)
class DashboardSnapshot:
    tracked_time: ChronoDisplayOutput
    current_app: str
    current_window: str
    last_app: str
    last_window: str
    last_observed_duration: ChronoDisplayOutput
    last_app_switch_at: DatetimeDisplayOutput
    sessions_emitted: int
    unique_apps_observed: int
    top_apps: tuple[TopAppsDisplayEntry, ...]
    recent_sessions: tuple[SessionDisplay, ...]