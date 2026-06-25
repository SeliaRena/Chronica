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
    Stylesheets,
    QIcons
)

from src.chronica.ui.widgets.common.factories import (
    icon_label,
    container
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
        self.portrait_label.setFixedSize(128, 128)
        self.portrait_label.setScaledContents(False)
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
        
        self.dialogue_states, states_layout = container(
            host=QFrame(frameShape=QFrame.Shape.NoFrame),
            host_object_name="dialogueStates",
            vertical=True,
            margins=(7, 7, 7, 7),
            spacing=10
        )
        
        self.dialogue_end_icon = icon_label(
            icon=QIcons.get("stop-circle.svg"),
            object_name="dialogueEndIcon",
            w=20,
            h=20
        )
        self.dialogue_end_icon.setToolTip("Current conversation has ended if this icon lights up.")
        
        self.next_line_icon = icon_label(
            icon=QIcons.get("next.png"),
            object_name="dialogueNextLineIcon",
            w=18,
            h=18
        )
        self.next_line_icon.setToolTip("You can click the dialogue box to adavance to the next line when this icon lights up.")
        
        self.skippable_icon = icon_label(
            icon=QIcons.get("fast-forward.png"),
            object_name="dialogueSkippableIcon",
            w=22,
            h=22
        )
        self.skippable_icon.setToolTip("You can click the dialogue box to instantly reveal the current line when this icon lights up.")
        
        self.dialogue_end_icon.setEnabled(False)
        self.next_line_icon.setEnabled(False)
        self.skippable_icon.setEnabled(True)
        
        if isinstance(states_layout, QVBoxLayout):
            states_layout.addWidget(self.dialogue_end_icon, alignment=Qt.AlignmentFlag.AlignHCenter)
            states_layout.addWidget(self.next_line_icon, alignment=Qt.AlignmentFlag.AlignHCenter)
            states_layout.addWidget(self.skippable_icon, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        dialogue_box_layout = QHBoxLayout()
        dialogue_box_layout.setContentsMargins(0, 0, 0, 0)
        dialogue_box_layout.setSpacing(10)
        dialogue_box_layout.addWidget(self.text_label, 1)
        dialogue_box_layout.addWidget(self.dialogue_states, 0)

        text_layout.addWidget(self.channel_label)
        text_layout.addWidget(self.speaker_label)
        text_layout.addLayout(dialogue_box_layout)

        root_layout.addWidget(self.portrait_label, 0)
        root_layout.addLayout(text_layout, 1)

        self.setStyleSheet(Stylesheets.load("dialogue_panel.qss"))
    
    def on_line_skippable(self, line_index: int, line_text: str) -> None:
        self.dialogue_end_icon.setEnabled(False)
        self.next_line_icon.setEnabled(False)
        self.skippable_icon.setEnabled(True)
    
    def on_next_line_confirmation_requested(self) -> None:
        self.dialogue_end_icon.setEnabled(False)
        self.next_line_icon.setEnabled(True)
        self.skippable_icon.setEnabled(False)
    
    def on_dialogue_ended(self) -> None:
        self.dialogue_end_icon.setEnabled(True)
        self.next_line_icon.setEnabled(False)
        self.skippable_icon.setEnabled(False)