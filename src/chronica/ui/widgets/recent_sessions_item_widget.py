from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QFrame,
    QSizePolicy
)

from PySide6.QtGui import (
    QFont,
    QIcon,
    QPixmap,
    QColor
)

from PySide6.QtCore import Qt, QSize

from src.chronica.ui.resources import (
    QIcons,
    Stylesheets
)

from src.chronica.ui.presentation.models import RecentSessionsItemData
from src.chronica.ui.widgets.elided_label import ElidedLabel
from src.chronica.ui.widgets.time_segment_indicator_widget import TimeSegmentIndicatorWidget

class RecentSessionsItemWidget(QWidget):
    CHIP_HEIGHT = 60
    MIN_ITEM_HEIGHT = 102
    
    def __init__(self, data: RecentSessionsItemData, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("recentSessionsItemWidget")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(self.MIN_ITEM_HEIGHT)
        self.data = data
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(0)
        
        # 1. Time labels
        time_labels = QWidget()
        time_labels.setObjectName("recentSessionsItemTimeLabels")
        time_layout = QVBoxLayout(time_labels)
        
        self.start_time_label = QLabel(self.data.start_time if self.data.is_first else "")
        self.start_time_label.setObjectName("recentSessionsItemStartTimeLabel")
        self.start_time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.start_time_label.setWordWrap(True)
        
        self.end_time_label = QLabel(self.data.end_time)
        self.end_time_label.setObjectName("recentSessionsItemEndTimeLabel")
        self.end_time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.end_time_label.setWordWrap(True)
        
        time_layout.addWidget(self.end_time_label, 1)
        time_layout.addWidget(self.start_time_label, 1)
        
        # 2. Time segment indicator
        line = QColor(201, 184, 255, 190)
        node = QColor("#7A5CFF")
        
        time_segment_indicator = TimeSegmentIndicatorWidget(
            show_bottom_node=True,
            show_top_node=True,
            fixed_height=None,
            bottom_padding=8,
            top_padding=8,
            line_width=3,
            node_radius=6,
            line_color=line,
            node_color=node,
            arrow_color=line,
        )
        
        # 3. Session Chip
        self.session_chip = QFrame()
        self.session_chip.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.session_chip.setFrameStyle(QFrame.Shape.NoFrame)
        self.session_chip.setObjectName("recentSessionsItemSessionChip")
        self.session_chip.setFixedHeight(self.CHIP_HEIGHT)
        
        chip_layout = QVBoxLayout(self.session_chip)
        chip_layout.setContentsMargins(7, 7, 7, 7)
        chip_layout.setSpacing(0)
        
        # 3-1r-1 Chip Icon
        chip_icon = QIcons.get("history.png")
        self.chip_icon_label = QLabel()
        self.chip_icon_label.setObjectName("recentSessionsItemChipIconLabel")
        self.chip_icon_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.chip_icon_label.setFixedSize(QSize(24, 24))
        self.chip_icon_label.setScaledContents(True)
        self.chip_icon_label.setPixmap(chip_icon.pixmap(24, 24))
        
        # 3-1r-2 First Row Data
        self.chip_app_name_label = ElidedLabel(self.data.app_name)
        self.chip_app_name_label.setObjectName("recentSessionsItemChipAppNameLabel")
        
        self.chip_duration_label = ElidedLabel(self.data.duration)
        self.chip_duration_label.setObjectName("recentSessionsItemChipDurationLabel")
        
        # First Row Layout
        first_row = QWidget()
        first_row.setObjectName("recentSessionsItemFirstRow")
        
        first_row_layout = QHBoxLayout(first_row)
        first_row_layout.setContentsMargins(0, 0, 0, 0)
        first_row_layout.setSpacing(8)
        
        first_row_layout.addWidget(self.chip_icon_label)
        first_row_layout.addWidget(self.chip_app_name_label)
        first_row_layout.addWidget(self.chip_duration_label)
        
        # 3-2r-1 Second Row Data
        self.chip_window_title_label = ElidedLabel(self.data.window_title)
        self.chip_window_title_label.setObjectName("recentSessionsItemChipWindowTitleLabel")
        self.chip_window_title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        # Assemble Chip Layout
        chip_layout.addWidget(first_row)
        chip_layout.addWidget(self.chip_window_title_label)
        
        # Assemble Main Layout
        layout.addWidget(time_labels, 0)
        layout.addWidget(time_segment_indicator, 1)
        layout.addWidget(self.session_chip, 4, alignment=Qt.AlignmentFlag.AlignVCenter)
        
        self.setStyleSheet(Stylesheets.load("recent_sessions_item_widget.qss"))