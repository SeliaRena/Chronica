from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.chronica.ui.resources import (
    QIcons,
    Stylesheets
)

from src.chronica.ui.widgets.common.factories import (
    container
)

from src.chronica.ui.widgets.common import PlainIconHeader
from src.chronica.ui.widgets.control_bar import ControlBarButton

class ControlBar(QFrame):
    dashboard_requested = Signal()
    tracking_archive_requested = Signal()
    settings_requested = Signal()

    start_requested = Signal()
    stop_requested = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("controlBar")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(14, 14, 14, 14)
        root_layout.setSpacing(5)

        title = QLabel("Chronica")
        title.setObjectName("controlBarTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.mode_label = QLabel("Mode: Idle")
        self.mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_hint_label = QLabel("Ready.")
        self.status_hint_label.setWordWrap(True)
        self.status_hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        root_layout.addWidget(title)
        root_layout.addWidget(self.mode_label)
        root_layout.addWidget(self.status_hint_label)

        root_layout.addSpacing(16)
        
        # nav section
        self.nav_section, nav_layout = container(
            QFrame(frameShape=QFrame.Shape.NoFrame),
            host_object_name="controlBarNavSection",
            vertical=True,
            margins=(10, 12, 10, 10),
            spacing=12
        )
        
        self.nav_buttons, buttons_layout = container(
            QFrame(frameShape=QFrame.Shape.NoFrame),
            host_object_name="controlBarNavButtons",
            vertical=True,
            margins=(0, 0, 0, 0),
            spacing=5
        )
        
        self.nav_header = PlainIconHeader(
            QIcons.get("navigation.png"),
            "Navigation",
            icon_w=24,
            icon_h=24,
            title_px=13,
        )

        self.dashboard_button = ControlBarButton(
            "Dashboard",
            icon=QIcons.get("dashboard-panel.svg"),
            icon_size=18,
        )
        
        self.tracking_archive_button = ControlBarButton(
            "Tracking Archive",
            icon=QIcons.get("archive.svg"),
            icon_size=18,
        )
        
        self.settings_button = ControlBarButton(
            "Settings",
            icon=QIcons.get("settings.svg"),
            icon_size=18,
        )

        buttons_layout.addWidget(self.dashboard_button)
        buttons_layout.addWidget(self.tracking_archive_button)
        buttons_layout.addWidget(self.settings_button)

        nav_layout.addWidget(self.nav_header)
        nav_layout.addWidget(self.nav_buttons)
        
        root_layout.addWidget(self.nav_section)
        root_layout.addSpacing(16)

        # tracking control section
        self.control_section, control_layout = container(
            QFrame(frameShape=QFrame.Shape.NoFrame),
            host_object_name="controlBarControlSection",
            vertical=True,
            margins=(10, 12, 10, 10),
            spacing=12
        )
        
        self.control_buttons, control_buttons_layout = container(
            QFrame(frameShape=QFrame.Shape.NoFrame),
            host_object_name="controlBarControlButtons",
            vertical=True,
            margins=(0, 0, 0, 0),
            spacing=5
        )
        
        self.control_header = PlainIconHeader(
            QIcons.get("eye.png"),
            "Tracking Controls",
            icon_w=24,
            icon_h=24,
            title_px=13,
        )
        
        self.start_button = ControlBarButton(
            "Start Tracking",
            icon=QIcons.get("power.svg"),
            icon_size=18,
        )
        
        self.stop_button = ControlBarButton(
            "Stop Tracking",
            icon=QIcons.get("stop-circle.svg"),
            icon_size=18,
        )
        self.stop_button.setEnabled(False)
        
        control_buttons_layout.addWidget(self.start_button)
        control_buttons_layout.addWidget(self.stop_button)

        control_layout.addWidget(self.control_header)
        control_layout.addWidget(self.control_buttons)

        root_layout.addWidget(self.control_section)
        root_layout.addStretch()

        # functional initialization
        self._connect_internal_signals()
        self.setStyleSheet(Stylesheets.load("control_bar.qss"))

    def _connect_internal_signals(self) -> None:
        self.dashboard_button.clicked.connect(self.dashboard_requested.emit)
        self.tracking_archive_button.clicked.connect(self.tracking_archive_requested.emit)
        self.settings_button.clicked.connect(self.settings_requested.emit)

        self.start_button.clicked.connect(self.start_requested.emit)
        self.stop_button.clicked.connect(self.stop_requested.emit)

    def set_tracking_idle(self) -> None:
        self.mode_label.setText("Mode: Idle")
        self.status_hint_label.setText("Ready.")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def set_tracking_running(self) -> None:
        self.mode_label.setText("Mode: Sampling")
        self.status_hint_label.setText("Tracking is active.")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def set_status_hint(self, text: str) -> None:
        self.status_hint_label.setText(text)

    def set_active_nav(self, page_name: str) -> None:
        buttons = {
            "dashboard": self.dashboard_button,
            "tracking archive": self.tracking_archive_button,
            "settings": self.settings_button,
        }

        for key, button in buttons.items():
            button.setProperty("active", key == page_name)
            button.style().unpolish(button)
            button.style().polish(button)
            button.update()