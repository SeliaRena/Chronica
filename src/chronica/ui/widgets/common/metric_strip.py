from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QFrame
)

from PySide6.QtCore import Qt

from src.chronica.ui.resources import (
    Stylesheets
)

class MetricStrip(QFrame):
    def __init__(self, title: str, value: str, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("metricStrip")
        self.setFrameShape(QFrame.StyledPanel)
        
        layout = QHBoxLayout(self)
        layout.setSpacing(7)
        layout.setContentsMargins(7, 7, 7, 7)
        
        self.title_label = QLabel(title)
        self.title_label.setObjectName("metricStripTitleLabel")
        self.title_label.setWordWrap(True)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.value_label = QLabel(value)
        self.value_label.setObjectName("metricStripValueLabel")
        self.value_label.setWordWrap(True)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        layout.addWidget(self.title_label, 1)
        layout.addWidget(self.value_label, 2)
        
        self.setStyleSheet(Stylesheets.load("common", "metric_strip.qss"))