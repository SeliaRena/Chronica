from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QFrame,
    QProgressBar,
    QSizePolicy
)

from PySide6.QtCore import Qt

from src.chronica.ui.resources import (
    Stylesheets
)

from src.chronica.ui.widgets.elided_label import ElidedLabel

class ProgressRow(QFrame):
    def __init__(self, title: str, subtitle: str, percentage: int, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("progressRow")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout(self)
        
        self.title_label = QLabel(f"{title}: {percentage}%")
        self.title_label.setObjectName("progressRowTitleLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.title_label.setWordWrap(False)
        
        self.subtitle_label = ElidedLabel(f"- {subtitle}")
        self.subtitle_label.setObjectName("progressRowSubtitleLabel")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.subtitle_label.setWordWrap(True)
        
        title_layout = QHBoxLayout()
        title_layout.addWidget(self.title_label, 0)
        title_layout.addWidget(self.subtitle_label, 1)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressRowProgressBar")
        self.progress_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(percentage)
        
        layout.addLayout(title_layout)
        layout.addWidget(self.progress_bar)
        
        self.setStyleSheet(Stylesheets.load("common", "progress_row.qss"))