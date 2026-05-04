from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel
)
from PySide6.QtGui import QFont

from src.chronica.ui.presentation.models import TrackingRecordDisplay
from src.chronica.ui.presentation.formatters import ymd_hms

class TrackingRecordItemWidget(QWidget):
    def __init__(self, record: TrackingRecordDisplay, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("trackingRecordItemWidget")
        self.record = record

        title_label = QLabel(self.record.title)
        title_label.setObjectName("titleLabel")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)

        description_label = QLabel(f"desc: {self.record.description}")
        description_label.setObjectName("descriptionLabel")
        description_font = QFont()
        description_font.setItalic(True)
        description_label.setFont(description_font)

        from_to_label = QLabel(f"{ymd_hms(self.record.start)} - {ymd_hms(self.record.end)}")
        from_to_label.setObjectName("fromToLabel")

        layout = QVBoxLayout(self)
        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addWidget(from_to_label)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(4)