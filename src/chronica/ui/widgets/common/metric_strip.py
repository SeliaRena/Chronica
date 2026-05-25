from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QFrame
)

class MetricStrip(QFrame):
    def __init__(self, title: str, value: str, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("metricStrip")
        self.setFrameShape(QFrame.StyledPanel)
        
        layout = QHBoxLayout(self)
        
        self.title_label = QLabel(title)
        self.title_label.setObjectName("titleLabel")
        self.title_label.setWordWrap(True)
        
        self.value_label = QLabel(value)
        self.value_label.setObjectName("valueLabel")
        self.value_label.setWordWrap(True)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)