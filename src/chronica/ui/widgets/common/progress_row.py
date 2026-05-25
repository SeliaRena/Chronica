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

class ProgressRow(QFrame):
    def __init__(self, title: str, subtitle: str, percentage: int, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("progressRow")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout(self)
        
        self.title_label = QLabel(title)
        self.title_label.setObjectName("titleLabel")
        self.title_label.setWordWrap(True)
        
        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setObjectName("subtitleLabel")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.subtitle_label.setWordWrap(True)
        
        title_layout = QHBoxLayout()
        title_layout.addWidget(self.title_label, 1)
        title_layout.addWidget(self.subtitle_label, 1)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(percentage)
        
        layout.addLayout(title_layout)
        layout.addWidget(self.progress_bar)