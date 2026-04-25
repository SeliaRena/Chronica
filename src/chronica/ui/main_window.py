from __future__ import annotations
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

from src.chronica.ui.dashboard_panel import DashboardPanel
from src.chronica.ui.control_bar import ControlBar
from src.chronica.ui.dialogue_panel import DialoguePanel
from src.chronica.ui.style_loader import load_stylesheet

class ChronicaMainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("chronicaMainWindow")
        self.setWindowTitle("Chronica")
        self.resize(1280, 800)
        self.setStyleSheet(load_stylesheet("main_window"))

        # 1. root
        root = QWidget()
        root.setObjectName("root")
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
        self.dialogue = DialoguePanel()
        self.control_bar = ControlBar()

        # 5. left side vertical arrangement
        left_layout.addWidget(self.dashboard, 5)
        left_layout.addWidget(self.dialogue, 2)

        # 6. outer horizontal arrangement
        root_layout.addWidget(left_container, 5)
        root_layout.addWidget(self.control_bar, 1)