from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QFrame
)

from PySide6.QtCore import Qt, QSize

from src.chronica.ui.widgets.common import (
    VMetricCard,
    ProgressRow,
    MetricStrip,
    IconHeader
)

from src.chronica.ui.resources import (
    Stylesheets,
    QIcons
)

from src.chronica.ui.presentation.models import WindowUsageItemData

class WindowUsageItemWidget(QFrame):
    def __init__(self, data: WindowUsageItemData, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("windowUsageItemWidget")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(7, 7, 7, 7)
        layout.setSpacing(7)
        
        # 1. Header
        self.header = IconHeader(
            icon=QIcons.load("browser.svg"),
            title=data.window_title,
            subtitle="",
        )
        self.header.setObjectName("windowItemHeader")
        
        # 2. Metric cards (Major stats)
        self.major_stats = QFrame()
        self.major_stats.setObjectName("windowItemMajorStats")
        self.major_stats.setFrameShape(QFrame.Shape.StyledPanel)
        major_stats_layout = QHBoxLayout(self.major_stats)
        
        self.usage_time_card = VMetricCard("Usage Time", data.total_usage_time)
        self.usage_time_card.setObjectName("windowItemUsageTimeCard")
        
        self.focus_count_card = VMetricCard("Focus Count", str(data.session_count))
        self.focus_count_card.setObjectName("windowItemFocusCountCard")
        
        major_stats_layout.addWidget(self.usage_time_card)
        major_stats_layout.addWidget(self.focus_count_card)
        
        # 3. Progress bars
        self.progress_bars = QFrame()
        self.progress_bars.setObjectName("windowItemProgressBars")
        self.progress_bars.setFrameShape(QFrame.Shape.StyledPanel)
        progress_bars_layout = QVBoxLayout(self.progress_bars)
        
        self.usage_ratio_row = ProgressRow("Usage Ratio", "", data.usage_ratio_percentage)
        self.focus_ratio_row = ProgressRow("Focus Ratio", "", data.session_ratio_percentage)
        
        progress_bars_layout.addWidget(self.usage_ratio_row)
        progress_bars_layout.addWidget(self.focus_ratio_row)
        
        # 4. Metric strips (Minor stats)
        self.minor_stats = QFrame()
        self.minor_stats.setObjectName("windowItemMinorStats")
        self.minor_stats.setFrameShape(QFrame.Shape.StyledPanel)
        minor_stats_layout = QVBoxLayout(self.minor_stats)
        
        self.longest_stay_strip = MetricStrip("Longest Stay", data.peak_session_duration)
        self.longest_absence_strip = MetricStrip("Longest Absence", data.peak_gap_duration)
        self.average_stay_strip = MetricStrip("Average Stay", data.avg_session_duration)
        self.first_used_at_strip = MetricStrip("First Used At", data.first_used_at)
        self.last_used_at_strip = MetricStrip("Last Used At", data.last_used_at)
        
        minor_stats_layout.addWidget(self.longest_stay_strip)
        minor_stats_layout.addWidget(self.longest_absence_strip)
        minor_stats_layout.addWidget(self.average_stay_strip)
        minor_stats_layout.addWidget(self.first_used_at_strip)
        minor_stats_layout.addWidget(self.last_used_at_strip)
        
        # 5. Assemble
        layout.addWidget(self.header)
        layout.addWidget(self.major_stats)
        layout.addWidget(self.progress_bars)
        layout.addWidget(self.minor_stats)