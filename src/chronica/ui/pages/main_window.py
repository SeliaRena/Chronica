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
    QStackedWidget
)

from src.chronica.ui.pages.dashboard_panel import DashboardPanel
from src.chronica.ui.pages.tracking_archive_panel import TrackingArchivePanel
from src.chronica.ui.pages.control_bar import ControlBar
from src.chronica.ui.pages.dialogue_panel import DialoguePanel
from src.chronica.ui.styles.style_loader import load_stylesheet
from src.chronica.common.runtime import AppRuntimeContext

class ChronicaMainWindow(QMainWindow):
    def __init__(self, app_ctx: AppRuntimeContext) -> None:
        super().__init__()
        self.app_ctx = app_ctx
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

        # 4. pages integration
        self.dashboard = DashboardPanel()
        self.tracking_archive = TrackingArchivePanel(self.app_ctx)
        
        self.main_section_stack = QStackedWidget()
        self.main_section_stack.addWidget(self.dashboard)
        self.main_section_stack.addWidget(self.tracking_archive)
        
        self.dialogue = DialoguePanel()
        self.control_bar = ControlBar()

        self.control_bar.tracking_archive_requested.connect(self.switch_to_tracking_archive)
        self.control_bar.dashboard_requested.connect(self.switch_to_dashboard)

        # 5. left side vertical arrangement
        left_layout.addWidget(self.main_section_stack, 5)
        left_layout.addWidget(self.dialogue, 2)

        # 6. outer horizontal arrangement
        root_layout.addWidget(left_container, 5)
        root_layout.addWidget(self.control_bar, 1)

    def switch_to_dashboard(self) -> None:
        self.control_bar.set_active_nav("dashboard")
        self.main_section_stack.setCurrentWidget(self.dashboard)

    def switch_to_tracking_archive(self) -> None:
        self.control_bar.set_active_nav("tracking archive")
        self.main_section_stack.setCurrentWidget(self.tracking_archive)