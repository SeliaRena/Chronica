from dataclasses import dataclass
from src.chronica.ui.presentation.models.general_display_models import SessionDisplay
from src.chronica.ui.presentation.models.top_apps_item_data import TopAppsItemData

type ChronoDisplayOutput = str
type DatetimeDisplayOutput = str

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
    top_apps: tuple[TopAppsItemData, ...]
    recent_sessions: tuple[SessionDisplay, ...]