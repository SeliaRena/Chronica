from src.chronica.domain.models import (
    Session,
    SessionHistory,
    WindowUsageInfo,
    AppUsageInfo,
    AppUsageReport,
    TrackingRecord
)

from src.chronica.ui.presentation.models import (
    WindowUsageItemData,
    AppUsageItemData,
    UsageReportData
)

from src.chronica.ui.presentation.formatters import (
    simplistic_simplified_ms,
    ymd_hms,
    hms,
    digital_clock_emphasis
)

from src.chronica.common.timestamp import TimestampContextProvider

class UsageReportDataMapper:
    def __init__(self, ts_ctx_provider: TimestampContextProvider) -> None:
        self.ts_ctx_provider = ts_ctx_provider
    
    def map(self, record: TrackingRecord) -> UsageReportData:
        return self._assemble_report_data(report=record.app_usage_report, history=record.session_history)
    
    def _assemble_windows(
        self,
        *,
        sorted_windowsinfo: list[WindowUsageInfo],
        app_session_count: int,
        app_usage_time_ms: int
    ) -> tuple[WindowUsageItemData, ...]:
        windows: list[WindowUsageItemData] = []
        ts_ctx = self.ts_ctx_provider.get()
        
        for windowinfo in sorted_windowsinfo:
            peak_session = windowinfo.peak_usage_session
            session_count = windowinfo.session_count
            
            windows.append(
                WindowUsageItemData(
                    window_title=windowinfo.window_title,
                    session_count=session_count,
                    session_ratio_in_app=session_count / app_session_count,
                    usage_ratio_in_app=windowinfo.total_usage_time_ms / app_usage_time_ms,
                    total_usage_time=simplistic_simplified_ms(windowinfo.total_usage_time_ms),
                    peak_session_duration=simplistic_simplified_ms(peak_session.duration),
                    peak_gap_duration=simplistic_simplified_ms(windowinfo.peak_gap_duration_ms),
                    avg_session_duration=simplistic_simplified_ms(windowinfo.avg_session_duration_ms),
                    first_used_at=ymd_hms(ts_ctx.datetime_from_ts_ms(windowinfo.first_used_ts_ms)),
                    last_used_at=ymd_hms(ts_ctx.datetime_from_ts_ms(windowinfo.last_used_ts_ms)),
                )
            )
        
        return tuple(windows)
    
    def _assemble_apps(
        self,
        *,
        sorted_appsinfo: list[AppUsageInfo],
        report_usage_time_ms: int,
        report_session_count: int,
        report_app_entry_count: int
    ) -> tuple[AppUsageItemData, ...]:
        apps: list[AppUsageItemData] = []
        ts_ctx = self.ts_ctx_provider.get()
        
        for appinfo in sorted_appsinfo:
            app_session_count = appinfo.session_count
            app_entry_count = appinfo.app_entry_count
            
            sorted_windowsinfo = sorted(
                appinfo.window_usage_map.values(),
                key=lambda windowinfo: windowinfo.total_usage_time_ms,
                reverse=True
            )
            
            apps.append(
                AppUsageItemData(
                    app_name=appinfo.app_name,
                    app_path=appinfo.app_path,
                    most_used_window=sorted_windowsinfo[0].window_title,
                    window_count=len(appinfo.window_usage_map),
                    session_count=app_session_count,
                    app_entry_count=app_entry_count,
                    usage_ratio_in_report=appinfo.total_usage_time_ms / report_usage_time_ms,
                    session_ratio_in_report=app_session_count / report_session_count,
                    app_entry_ratio_in_report=app_entry_count / report_app_entry_count,
                    usage_time_digital=digital_clock_emphasis(appinfo.total_usage_time_ms),
                    total_usage_time=simplistic_simplified_ms(appinfo.total_usage_time_ms),
                    avg_session_duration=simplistic_simplified_ms(appinfo.total_usage_time_ms // app_session_count),
                    avg_app_entry_duration=simplistic_simplified_ms(appinfo.total_usage_time_ms // app_entry_count),
                    first_used_at=ymd_hms(ts_ctx.datetime_from_ts_ms(appinfo.first_used_ts_ms)),
                    last_used_at=ymd_hms(ts_ctx.datetime_from_ts_ms(appinfo.last_used_ts_ms)),
                    windows=self._assemble_windows(
                        sorted_windowsinfo=sorted_windowsinfo,
                        app_session_count=app_session_count,
                        app_usage_time_ms=appinfo.total_usage_time_ms
                    ),
                )
            )
        
        return tuple(apps)
        
    def _assemble_report_data(
        self,
        *,
        report: AppUsageReport,
        history: SessionHistory
    ) -> UsageReportData:
        ts_ctx = self.ts_ctx_provider.get()
        total_app_entry_count = report.total_app_entry_count
        total_session_count = len(history)
        first_used_ts_ms = history.require_oldest.start_ts_ms
        last_used_ts_ms = history.require_latest.end_ts_ms

        peak_session = max(
            (s for s in history.chronological_sessions),
            key=lambda s: s.duration
        )
        
        sorted_appsinfo = sorted(
            report.app_usage_map.values(), 
            key=lambda appinfo: appinfo.total_usage_time_ms, 
            reverse=True
        )
        
        return UsageReportData(
            most_used_app=sorted_appsinfo[0].app_name,
            peak_session_app_name=peak_session.app_name,
            peak_session_window_title=peak_session.window_title,
            app_count=len(report.app_usage_map),
            total_session_count=total_session_count,
            total_app_entry_count=total_app_entry_count,
            total_usage_time=simplistic_simplified_ms(report.total_usage_time_ms),
            peak_session_duration=simplistic_simplified_ms(peak_session.duration),
            avg_session_duration=simplistic_simplified_ms(report.total_usage_time_ms // total_session_count),
            avg_app_entry_duration=simplistic_simplified_ms(report.total_usage_time_ms // total_app_entry_count),
            first_used_at=ymd_hms(ts_ctx.datetime_from_ts_ms(first_used_ts_ms)),
            last_used_at=ymd_hms(ts_ctx.datetime_from_ts_ms(last_used_ts_ms)),
            apps=self._assemble_apps(
                sorted_appsinfo=sorted_appsinfo,
                report_usage_time_ms=report.total_usage_time_ms,
                report_session_count=total_session_count,
                report_app_entry_count=total_app_entry_count
            ),
        )