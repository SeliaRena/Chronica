from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, 
    QLabel, 
    QFrame, 
    QHBoxLayout
)

from src.chronica.ui.resources import (
    Stylesheets
)

class DigitalTimeStrip(QWidget):
    def __init__(
        self,
        title: str,
        shaded: str,
        emphasized: str,
        *,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)

        self.setObjectName("digitalTimeStrip")

        self._title_label = QLabel(title)
        self._title_label.setObjectName("digitalTimeStripTitle")

        self._shaded_segment = QFrame()
        self._shaded_segment.setObjectName("digitalTimeShadedSegment")

        self._shaded_label = QLabel(shaded)
        self._shaded_label.setObjectName("digitalTimeShadedLabel")
        self._shaded_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        shaded_layout = QHBoxLayout(self._shaded_segment)
        shaded_layout.setContentsMargins(8, 4, 8, 4)
        shaded_layout.setSpacing(0)
        shaded_layout.addWidget(self._shaded_label)

        self._emphasized_segment = QFrame()
        self._emphasized_segment.setObjectName("digitalTimeEmphasizedSegment")

        self._emphasized_label = QLabel(emphasized)
        self._emphasized_label.setObjectName("digitalTimeEmphasizedLabel")
        self._emphasized_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        emphasized_layout = QHBoxLayout(self._emphasized_segment)
        emphasized_layout.setContentsMargins(10, 4, 10, 4)
        emphasized_layout.setSpacing(0)
        emphasized_layout.addWidget(self._emphasized_label)

        time_layout = QHBoxLayout()
        time_layout.setContentsMargins(0, 0, 0, 0)
        time_layout.setSpacing(6)
        time_layout.addWidget(self._shaded_segment)
        time_layout.addWidget(self._emphasized_segment)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 6, 10, 6)
        main_layout.setSpacing(12)
        main_layout.addWidget(self._title_label, stretch=1)
        main_layout.addLayout(time_layout)
        
        self.setStyleSheet(Stylesheets.load("common", "digital_time_strip.qss"))

    def set_time(self, shaded: str, emphasized: str) -> None:
        self._shaded_label.setText(shaded)
        self._emphasized_label.setText(emphasized)

    def set_title(self, title: str) -> None:
        self._title_label.setText(title)