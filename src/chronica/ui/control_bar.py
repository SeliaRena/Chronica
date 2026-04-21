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

class ControlBar(QFrame):
    dashboard_requested = Signal()
    sessions_requested = Signal()
    reports_requested = Signal()
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
        root_layout.setSpacing(12)

        title = QLabel("Chronica")
        title_font = QFont()
        title_font.setPointSize(15)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.mode_label = QLabel("Mode: Idle")
        self.mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_hint_label = QLabel("Ready.")
        self.status_hint_label.setWordWrap(True)
        self.status_hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        root_layout.addWidget(title)
        root_layout.addWidget(self.mode_label)
        root_layout.addWidget(self.status_hint_label)

        root_layout.addSpacing(10)

        self.dashboard_button = QPushButton("Dashboard")
        self.sessions_button = QPushButton("Sessions")
        self.reports_button = QPushButton("Reports")
        self.settings_button = QPushButton("Settings")

        root_layout.addWidget(self.dashboard_button)
        root_layout.addWidget(self.sessions_button)
        root_layout.addWidget(self.reports_button)
        root_layout.addWidget(self.settings_button)

        root_layout.addSpacing(16)

        self.start_button = QPushButton("Start Tracking")
        self.stop_button = QPushButton("Stop Tracking")
        self.stop_button.setEnabled(False)

        root_layout.addWidget(self.start_button)
        root_layout.addWidget(self.stop_button)

        root_layout.addStretch()

        self._connect_internal_signals()
        self._apply_styles()

    def _connect_internal_signals(self) -> None:
        self.dashboard_button.clicked.connect(self.dashboard_requested.emit)
        self.sessions_button.clicked.connect(self.sessions_requested.emit)
        self.reports_button.clicked.connect(self.reports_requested.emit)
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
            "sessions": self.sessions_button,
            "reports": self.reports_button,
            "settings": self.settings_button,
        }

        for key, button in buttons.items():
            button.setProperty("active", key == page_name)
            button.style().unpolish(button)
            button.style().polish(button)
            button.update()

    def _apply_styles(self) -> None:
        self.setStyleSheet(
            """
            QFrame#controlBar {
                background-color: #1d2129;
                border: 1px solid #2b3240;
                border-radius: 12px;
            }

            QLabel {
                color: #e8ecf1;
            }

            QPushButton {
                background-color: #2b3240;
                color: #e8ecf1;
                border: 1px solid #3a4457;
                border-radius: 8px;
                padding: 10px 12px;
                text-align: left;
            }

            QPushButton:hover {
                background-color: #364055;
            }

            QPushButton:disabled {
                background-color: #22262f;
                color: #8b93a3;
            }

            QPushButton[active="true"] {
                background-color: #46546f;
                border: 1px solid #64748b;
                font-weight: bold;
            }
            """
        )