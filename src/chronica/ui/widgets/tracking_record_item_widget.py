from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QFrame,
    QSizePolicy
)

from PySide6.QtCore import Qt

from src.chronica.ui.resources import (
    Stylesheets,
    QIcons
)

from src.chronica.ui.presentation.formatters import (
    simplistic_simplified_ms,
    ymd_hms
)

from src.chronica.ui.widgets.common import (
    PlainIconHeader
)

from src.chronica.ui.widgets.common.factories import (
    icon_button
)

from src.chronica.ui.presentation.models import TrackingRecordDisplay

class TrackingRecordItemWidget(QFrame):
    def __init__(self, record: TrackingRecordDisplay, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("trackingRecordItemWidget")
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.record = record

        self.header = PlainIconHeader(
            QIcons.get("order-history.png"),
            record.title,
            icon_w=24,
            icon_h=24,
            title_px=12,
            compress_content_left=False,
        )
        
        # start / end time labels
        self.time_labels = QFrame(frameShape=QFrame.Shape.NoFrame)
        time_layout = QVBoxLayout(self.time_labels)
        time_layout.setContentsMargins(0, 0, 0, 0)
        time_layout.setSpacing(5)
        
        self.start_time_label = QLabel(ymd_hms(record.start))
        self.start_time_label.setObjectName("recordItemStartTimeLabel")
        self.end_time_label = QLabel(f"➝ {ymd_hms(record.end)}")
        self.end_time_label.setObjectName("recordItemEndTimeLabel")
        
        time_layout.addWidget(self.start_time_label)
        time_layout.addWidget(self.end_time_label)
        
        # icon buttons
        self.icon_buttons = QFrame(frameShape=QFrame.Shape.NoFrame)
        buttons_layout = QHBoxLayout(self.icon_buttons)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(5)
        
        self.edit_button = icon_button(
            QIcons.get("file-edit.svg"),
            button_size=20,
            icon_size=16,
            object_name="recordItemEditButton",
            tooltip="Edit attributes of this record"
        )
        
        self.info_button = icon_button(
            QIcons.get("info.svg"),
            button_size=20,
            icon_size=16,
            object_name="recordItemInfoButton",
            tooltip="Let Chronica tells you more about this record"
        )
        
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.info_button)
        
        # Assemble
        self.content = QFrame(frameShape=QFrame.Shape.NoFrame)
        content_layout = QHBoxLayout(self.content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(5)
        content_layout.addWidget(self.time_labels, 0)
        content_layout.addWidget(self.icon_buttons, alignment=Qt.AlignmentFlag.AlignLeft)
        content_layout.addStretch()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 5, 12, 5)
        layout.setSpacing(5)
        layout.addWidget(self.header)
        layout.addWidget(self.content)
        
        self.setStyleSheet(Stylesheets.load("tracking_record_item_widget.qss"))