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

from src.chronica.common.resource_locator import ResourceLocator
from src.chronica.ui.styles.style_loader import load_stylesheet
from src.chronica.ui.resources.font_loader import load_font
from src.chronica.ui.controllers.typewriter_controller import TypewriterController
from src.chronica.characters.chronica.dialogues import random_pick_dialogue, Scenario

_TYPEWRITER_DELAY = 10

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

        self.typewriter = TypewriterController(self.text_label, _TYPEWRITER_DELAY)
        self.set_dialogue("Chronica", random_pick_dialogue(Scenario.BOOTUP))

        text_layout.addWidget(self.channel_label)
        text_layout.addWidget(self.speaker_label)
        text_layout.addWidget(self.text_label, 1)

        root_layout.addWidget(self.portrait_label, 0)
        root_layout.addLayout(text_layout, 1)

        self.setStyleSheet(load_stylesheet("dialogue_panel"))

    def set_dialogue(
        self,
        speaker: str,
        text: str,
        channel: str = "SYSTEM CHANNEL",
        portrait_text: str | None = None,
    ) -> None:
        self.channel_label.setText(channel)
        self.speaker_label.setText(speaker)
        self.typewriter.start(text)

        if portrait_text is not None:
            self.portrait_label.setText(portrait_text)
        else:
            self.portrait_label.setText(speaker)