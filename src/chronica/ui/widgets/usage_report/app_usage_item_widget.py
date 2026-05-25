from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QFrame,
    QSizePolicy
)

from PySide6.QtCore import Qt, QSize

from src.chronica.ui.widgets.common import (
    VMetricCard,
    ProgressRow,
    MetricStrip,
    IconHeader,
    ExpandableSection,
    DigitalTimeStrip
)

from src.chronica.ui.resources import (
    Stylesheets,
    QIcons,
    AppIconProvider
)

from src.chronica.ui.presentation.models import AppUsageItemData
from src.chronica.ui.widgets.usage_report.window_usage_item_widget import WindowUsageItemWidget

class AppUsageItemWidget(QFrame):
    def __init__(self, data: AppUsageItemData, app_icon_provider: AppIconProvider, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("appUsageItemWidget")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.data = data
        self.app_icon_provider = app_icon_provider

        layout = QVBoxLayout(self)
        
        # 1. Header
        self.header = IconHeader(
            icon=self.app_icon_provider.icon_for_path(self.data.app_path),
            title=self.data.app_name,
            subtitle=self.data.app_path,
        )
        
        # 2. Digital Time Strip
        digital_time = self.data.usage_time_digital
        self.digital_time_strip = DigitalTimeStrip(
            title="Usage Time",
            shaded=digital_time.shaded,
            emphasized=digital_time.emphasized,
        )
        
        # 3. Major stats
        self.major_stats = QFrame()
        self.major_stats.setObjectName("appItemMajorStats")
        self.major_stats.setFrameShape(QFrame.Shape.StyledPanel)
        major_stats_layout = QHBoxLayout(self.major_stats)
        
        self.focus_count_card = VMetricCard("Focus Count", str(self.data.session_count))
        self.entry_count_card = VMetricCard("Entry Count", str(self.data.app_entry_count))
        self.window_count_card = VMetricCard("Window Count", str(self.data.window_count))
        self.most_used_window_card = VMetricCard("Most Used Window", self.data.most_used_window)
        
        major_stats_layout.addWidget(self.focus_count_card)
        major_stats_layout.addWidget(self.entry_count_card)
        major_stats_layout.addWidget(self.window_count_card)
        major_stats_layout.addWidget(self.most_used_window_card)
        
        # 4. Progress Rows (Expandable content from now on)
        self.progress_rows = QFrame()
        self.progress_rows.setObjectName("appItemProgressRows")
        self.progress_rows.setFrameShape(QFrame.Shape.StyledPanel)
        progress_rows_layout = QVBoxLayout(self.progress_rows)
        
        self.usage_ratio_row = ProgressRow(
            title="Usage Ratio", 
            subtitle="", 
            percentage=self.data.usage_ratio_percentage
        )
        
        self.focus_ratio_row = ProgressRow(
            title="Focus Ratio", 
            subtitle="window switches included.", 
            percentage=self.data.session_ratio_percentage
        )
        
        self.entry_ratio_row = ProgressRow(
            title="Entry Ratio", 
            subtitle="window switches excluded.", 
            percentage=self.data.app_entry_ratio_percentage
        )
        
        progress_rows_layout.addWidget(self.usage_ratio_row)
        progress_rows_layout.addWidget(self.focus_ratio_row)
        progress_rows_layout.addWidget(self.entry_ratio_row)
        
        # 5. Minor Stats
        self.minor_stats = QFrame()
        self.minor_stats.setObjectName("appItemMinorStats")
        self.minor_stats.setFrameShape(QFrame.Shape.StyledPanel)
        minor_stats_layout = QVBoxLayout(self.minor_stats)
        
        self.average_stay_strip = MetricStrip("Average Stay", self.data.avg_session_duration)
        self.average_entry_duration_strip = MetricStrip("Average Entry Duration", self.data.avg_app_entry_duration)
        self.first_used_at_strip = MetricStrip("First Used At", self.data.first_used_at)
        self.last_used_at_strip = MetricStrip("Last Used At", self.data.last_used_at)
        
        minor_stats_layout.addWidget(self.average_stay_strip)
        minor_stats_layout.addWidget(self.average_entry_duration_strip)
        minor_stats_layout.addWidget(self.first_used_at_strip)
        minor_stats_layout.addWidget(self.last_used_at_strip)
        
        # 6. Window Items (Internal expandable content)
        self.window_items = QFrame()
        self.window_items.setObjectName("appItemWindowItems")
        self.window_items.setFrameShape(QFrame.Shape.StyledPanel)
        window_items_layout = QVBoxLayout(self.window_items)
        
        for window_item_data in self.data.windows:
            window_items_layout.addWidget(WindowUsageItemWidget(window_item_data))
        
        self.window_items_expand_toggle = ExpandableSection(
            title="Click to view window usage details.",
            content=self.window_items,
            initially_expanded=False,
        )
        
        # 7. Assemble
        self.app_details_expand_toggle = ExpandableSection(
            title="Click to view app details.",
            content=None,
            initially_expanded=False,
        )

        self.app_details_expand_toggle.add_widget(self.progress_rows)
        self.app_details_expand_toggle.add_widget(self.minor_stats)
        self.app_details_expand_toggle.add_widget(self.window_items_expand_toggle)

        layout.addWidget(self.header)
        layout.addWidget(self.digital_time_strip)
        layout.addWidget(self.major_stats)
        layout.addWidget(self.app_details_expand_toggle)