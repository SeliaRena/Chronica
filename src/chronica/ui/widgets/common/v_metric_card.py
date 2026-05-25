from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame
)

from src.chronica.ui.resources import (
    Stylesheets
)

class VMetricCard(QFrame):
    def __init__(self, title: str, value: str, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("vMetricCard")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        self.title_label = QLabel(title)
        self.title_label.setObjectName("titleLabel")
        self.title_label.setWordWrap(True)
        
        self.value_label = QLabel(value)
        self.value_label.setObjectName("valueLabel")
        self.value_label.setWordWrap(True)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)