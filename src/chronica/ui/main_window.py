from __future__ import annotations
from src.chronica.ui.dashboard_panel import DashboardPanel
from src.chronica.ui.control_bar import ControlBar
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QPixmap, QAction
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

class ChronicaMainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Chronica")
        self.resize(1280, 800)

        # 1. root
        root = QWidget()
        self.setCentralWidget(root)

        # 2. root layout: horizontal split
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(12, 12, 12, 12)
        root_layout.setSpacing(12)

        # 3. left container: vertical split
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(12)

        # 4. three main sections: dashboard, dialogue panel, control bar
        self.dashboard = DashboardPanel()
        self.dialogue = self._make_placeholder("Dialogue Panel")
        self.control_bar = ControlBar()

        # 5. left side vertical arrangement
        left_layout.addWidget(self.dashboard, 5)
        left_layout.addWidget(self.dialogue, 2)

        # 6. outer horizontal arrangement
        root_layout.addWidget(left_container, 5)
        root_layout.addWidget(self.control_bar, 1)

    def _make_placeholder(self, title: str) -> QFrame:
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(frame)
        label = QLabel(title)
        layout.addWidget(label)

        frame.setStyleSheet(
            """
            QFrame {
                background: #1e1f22;
                border: 1px solid #3a3d41;
                border-radius: 10px;
            }
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
            """
        )
        return frame