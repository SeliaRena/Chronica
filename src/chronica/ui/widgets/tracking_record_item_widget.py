from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel
)
from PySide6.QtGui import QFont

from src.chronica.domain.tracking_record import TrackingRecord
from src.chronica.ui.data_display.datetime_format import ymd_hms

class TrackingRecordItemWidget(QWidget):
    def __init__(self, tracking_record: TrackingRecord, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("trackingRecordItemWidget")
        self.tracking_record = tracking_record
        
        title_label = QLabel(self.tracking_record.title)
        title_label.setObjectName("titleLabel")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)

        description_label = QLabel(f"desc: {self.tracking_record.description}")
        description_label.setObjectName("descriptionLabel")
        description_font = QFont()
        description_font.setItalic(True)
        description_label.setFont(description_font)

        from_to_label = QLabel(f"{ymd_hms(self.tracking_record.start_ts_ms)} - {ymd_hms(self.tracking_record.end_ts_ms)}")
        from_to_label.setObjectName("fromToLabel")

        layout = QVBoxLayout(self)
        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addWidget(from_to_label)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(4)