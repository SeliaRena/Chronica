from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QLabel

from src.chronica.characters.dialogue_player import DialoguePlayer

from src.chronica.characters.dialogues import (
    Scenario,
    DialogueDatabase,
    CHRONICA_DIALOGUE_DATABASE
)

from src.chronica.characters.models import (
    Line,
    DialogueRenderContext,
    DialogueKey,
    DialogueTemplate,
    RenderedDialogue
)

import random

class Character(QObject):
    started_speaking = Signal(object, str, object)
    finished_speaking = Signal()
    current_dialogue_cancelled = Signal()
    
    line_skippable = Signal(int, str)
    next_line_confirmation_requested = Signal()
    
    def __init__(
        self,
        dialogue_box: QLabel,
        database: DialogueDatabase = CHRONICA_DIALOGUE_DATABASE,
        *,
        parent: QObject | None = None
    ) -> None:
        super().__init__(parent)
        
        self._player: DialoguePlayer = DialoguePlayer(
            bound_label=dialogue_box, 
            autoplay=False,
            parent=self,
        )
        
        self._database = database
        self._speaking: bool = False
        
        self._player.dialogue_finished.connect(self._on_player_finished)
        self._player.line_started.connect(self.line_skippable)
        self._player.confirmation_requested.connect(self.next_line_confirmation_requested)
    
    @property
    def speaking(self) -> bool:
        return self._speaking
    
    def say_random(self, scenario: Scenario) -> None:
        if self._speaking:
            self._cancel_speaking()

        picked_dialogue = random.choice(list(self._database[scenario].values()))
        rendered_without_context = picked_dialogue.render()
        
        self._speaking = True
        self.started_speaking.emit(scenario, picked_dialogue.key, rendered_without_context)
        self._player.play(rendered_without_context)
    
    def say_certain(self, scenario: Scenario, dialogue_key: DialogueKey, context: DialogueRenderContext) -> None:
        if dialogue_key not in self._database[scenario]:
            raise ValueError(f"Unknown dialogue key: {dialogue_key}")
        
        if self._speaking:
            self._cancel_speaking()
        
        rendered = self._database[scenario][dialogue_key].render(context)
        
        self._speaking = True
        self.started_speaking.emit(scenario, dialogue_key, rendered)
        self._player.play(rendered)
    
    def _cancel_speaking(self) -> None:
        self._player.stop()
        self._speaking = False
        self.current_dialogue_cancelled.emit()
    
    @Slot()
    def _on_player_finished(self) -> None:
        self._speaking = False
        self.finished_speaking.emit()