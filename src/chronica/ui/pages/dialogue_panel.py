from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.chronica.ui.resources import (
    Stylesheets
)

class DialoguePanel(QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("dialoguePanel")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFixedHeight(180)

        root_layout = QHBoxLayout(self)
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(14)

        # Left: portrait / identity block
        self.portrait_label = QLabel("Chronica")
        self.portrait_label.setObjectName("dialoguePortrait")
        self.portrait_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.portrait_label.setFixedSize(116, 116)
        self.portrait_label.setWordWrap(True)

        # Right: text block
        text_layout = QVBoxLayout()
        text_layout.setSpacing(6)

        self.channel_label = QLabel("SYSTEM CHANNEL")
        self.channel_label.setObjectName("dialogueChannel")

        self.speaker_label = QLabel("Chronica")
        self.speaker_label.setObjectName("dialogueSpeaker")
        
        self.text_label = QLabel()
        self.text_label.setObjectName("dialogueText")
        self.text_label.setWordWrap(True)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        text_layout.addWidget(self.channel_label)
        text_layout.addWidget(self.speaker_label)
        text_layout.addWidget(self.text_label, 1)

        root_layout.addWidget(self.portrait_label, 0)
        root_layout.addLayout(text_layout, 1)

        self.setStyleSheet(Stylesheets.load("dialogue_panel.qss"))