from __future__ import annotations

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QLabel

from src.chronica.ui.controllers.typewriter_controller import (
    TypewriterController,
)

from src.chronica.characters.models import RenderedDialogue
from src.chronica.characters.chronica.resources import Expressions

class DialoguePlayer(QObject):
    dialogue_started = Signal()
    dialogue_finished = Signal()
    dialogue_interrupted = Signal()

    line_started = Signal(int, str)
    line_finished = Signal(int, str)
    confirmation_requested = Signal()

    def __init__(
        self,
        bound_label: QLabel,
        bound_expression_label: QLabel,
        *,
        autoplay: bool = True,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)

        self._bound_expression_label = bound_expression_label
        # init the default expression to "smug"
        self._bound_expression_label.setPixmap(Expressions.get("smug"))
        
        self._typewriter = TypewriterController(
            target_label=bound_label,
            interval_ms=20,
            parent=self,
        )

        self._autoplay = autoplay

        self._current_dialogue: RenderedDialogue | None = None
        self._line_index = 0
        self._playing = False
        self._awaiting_confirmation = False

        self._typewriter.finished.connect(
            self._on_typewriter_finished
        )
        self._typewriter.advance_requested.connect(
            self.confirm
        )

    @property
    def playing(self) -> bool:
        return self._playing

    @property
    def autoplay(self) -> bool:
        return self._autoplay

    @property
    def awaiting_confirmation(self) -> bool:
        return self._awaiting_confirmation

    def set_autoplay(self, autoplay: bool) -> None:
        self._autoplay = autoplay

        # 如果當前已經在等待確認，切換成 autoplay 後立即繼續。
        if autoplay and self._awaiting_confirmation:
            self.confirm()

    def play(
        self,
        dialogue: RenderedDialogue,
        *,
        autoplay: bool | None = None,
    ) -> None:
        if self._playing:
            self.stop()

        if autoplay is not None:
            self._autoplay = autoplay

        self._current_dialogue = dialogue
        self._line_index = 0
        self._playing = True
        self._awaiting_confirmation = False

        self.dialogue_started.emit()

        if not dialogue.lines:
            self._finish()
            return

        self._play_current_line()

    def stop(self) -> None:
        if not self._playing:
            return

        self._typewriter.stop(
            clear=False,
            emit_stopped=False,
        )

        self._clear_states()
        self.dialogue_interrupted.emit()

    @Slot()
    def confirm(self) -> None:
        """
        Confirm the currently displayed line and proceed.

        Does nothing while the typewriter is still running, because clicking
        during typing is handled as a skip by TypewriterController.
        """

        if not self._playing:
            return

        if not self._awaiting_confirmation:
            return

        self._awaiting_confirmation = False
        self._advance()

    def _play_current_line(self) -> None:
        dialogue = self._current_dialogue

        if dialogue is None:
            return

        text = dialogue.lines[self._line_index].text
        expression = dialogue.lines[self._line_index].expression
        
        if expression:
            pixmap = Expressions.get(expression)
            self._bound_expression_label.setPixmap(pixmap)

        self._awaiting_confirmation = False
        self.line_started.emit(self._line_index, text)
        self._typewriter.start(text)

    @Slot()
    def _on_typewriter_finished(self) -> None:
        dialogue = self._current_dialogue

        if not self._playing or dialogue is None:
            return

        text = dialogue.lines[self._line_index].text
        self.line_finished.emit(self._line_index, text)

        if self._autoplay:
            self._advance()
            return

        self._awaiting_confirmation = True
        self.confirmation_requested.emit()

    def _advance(self) -> None:
        self._line_index += 1

        dialogue = self._current_dialogue

        if dialogue is None:
            return

        if self._line_index >= len(dialogue.lines):
            self._finish()
            return

        self._play_current_line()

    def _finish(self) -> None:
        # switch back to default expression when dialogue finishes
        self._bound_expression_label.setPixmap(Expressions.get("smug"))

        self._clear_states()
        self.dialogue_finished.emit()

    def _clear_states(self) -> None:
        self._current_dialogue = None
        self._line_index = 0
        self._playing = False
        self._awaiting_confirmation = False