from __future__ import annotations
from dataclasses import dataclass

from src.chronica.ui.presentation.formatters import DigitalTimeEmphasis

type FormattedDatetime = str
type FormattedCascadedSpan = str

@dataclass(frozen=True, slots=True)
class WindowUsageItemData:
    window_title         : str
    session_count        : int
    session_ratio_in_app : float
    usage_ratio_in_app   : float
    total_usage_time     : FormattedCascadedSpan
    peak_session_duration: FormattedCascadedSpan
    peak_gap_duration    : FormattedCascadedSpan
    avg_session_duration : FormattedCascadedSpan
    first_used_at        : FormattedDatetime
    last_used_at         : FormattedDatetime
    
    @property
    def usage_ratio_percentage(self) -> int:
        return int(self.usage_ratio_in_app * 100)

    @property
    def session_ratio_percentage(self) -> int:
        return int(self.session_ratio_in_app * 100)

@dataclass(frozen=True, slots=True)
class AppUsageItemData:
    app_name                 : str
    app_path                 : str
    most_used_window         : str
    window_count             : int
    session_count            : int
    app_entry_count          : int
    usage_ratio_in_report    : float
    session_ratio_in_report  : float
    app_entry_ratio_in_report: float
    usage_time_digital       : DigitalTimeEmphasis
    total_usage_time         : FormattedCascadedSpan
    avg_session_duration     : FormattedCascadedSpan
    avg_app_entry_duration   : FormattedCascadedSpan
    first_used_at            : FormattedDatetime
    last_used_at             : FormattedDatetime
    windows                  : tuple[WindowUsageItemData, ...]

    @property
    def usage_ratio_percentage(self) -> int:
        return int(self.usage_ratio_in_report * 100)

    @property
    def session_ratio_percentage(self) -> int:
        return int(self.session_ratio_in_report * 100)

    @property
    def app_entry_ratio_percentage(self) -> int:
        return int(self.app_entry_ratio_in_report * 100)
    
@dataclass(frozen=True, slots=True)
class UsageReportData:
    most_used_app            : str
    peak_session_app_name    : str
    peak_session_window_title: str
    app_count                : int
    total_session_count      : int
    total_app_entry_count    : int
    total_usage_time         : FormattedCascadedSpan
    peak_session_duration    : FormattedCascadedSpan
    avg_session_duration     : FormattedCascadedSpan
    avg_app_entry_duration   : FormattedCascadedSpan
    first_used_at            : FormattedDatetime
    last_used_at             : FormattedDatetime
    apps                     : tuple[AppUsageItemData, ...]