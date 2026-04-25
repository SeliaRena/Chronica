from __future__ import annotations

from PySide6.QtCore import QObject, QTimer, Signal
from PySide6.QtWidgets import QLabel


class TypewriterController(QObject):
    """
    Controls a typewriter text effect for a QLabel.

    Responsibilities:
    - Reveal text character by character.
    - Allow skipping to full text.
    - Allow stopping / clearing.
    - Emit signals when started, updated, finished, or skipped.

    This class belongs to the presentation layer because it directly depends on Qt widgets.
    """

    started = Signal()
    updated = Signal(str)
    finished = Signal()
    skipped = Signal()

    def __init__(
        self,
        target_label: QLabel,
        interval_ms: int = 30,
        parent: QObject | None = None,
    ):
        super().__init__(parent)

        self._target_label = target_label
        self._interval_ms = interval_ms

        self._full_text: str = ""
        self._current_index: int = 0
        self._is_running: bool = False

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._step)

    @property
    def is_running(self) -> bool:
        return self._is_running

    @property
    def full_text(self) -> str:
        return self._full_text

    @property
    def interval_ms(self) -> int:
        return self._interval_ms

    def set_interval(self, interval_ms: int) -> None:
        if interval_ms <= 0:
            raise ValueError("interval_ms must be greater than 0.")

        self._interval_ms = interval_ms

        if self._timer.isActive():
            self._timer.start(self._interval_ms)

    def start(self, text: str, interval_ms: int | None = None) -> None:
        """
        Start typing a new piece of text.

        If another typewriter effect is running, it will be replaced.
        """

        if interval_ms is not None:
            self.set_interval(interval_ms)

        self.stop(clear=False)

        self._full_text = text
        self._current_index = 0
        self._is_running = True

        self._target_label.setText("")
        self.started.emit()

        if not text:
            self._finish()
            return

        self._timer.start(self._interval_ms)

    def stop(self, clear: bool = False) -> None:
        """
        Stop the typewriter effect.

        If clear=True, also clears the label text.
        """

        self._timer.stop()
        self._is_running = False

        if clear:
            self._target_label.setText("")
            self.updated.emit("")

    def skip(self) -> None:
        """
        Immediately reveal the full text.
        """

        if not self._is_running:
            return

        self._timer.stop()
        self._target_label.setText(self._full_text)
        self._current_index = len(self._full_text)
        self._is_running = False

        self.updated.emit(self._full_text)
        self.skipped.emit()
        self.finished.emit()

    def clear(self) -> None:
        self.stop(clear=True)
        self._full_text = ""
        self._current_index = 0

    def _step(self) -> None:
        if self._current_index >= len(self._full_text):
            self._finish()
            return

        self._current_index += 1
        visible_text = self._full_text[:self._current_index]

        self._target_label.setText(visible_text)
        self.updated.emit(visible_text)

        if self._current_index >= len(self._full_text):
            self._finish()

    def _finish(self) -> None:
        self._timer.stop()
        self._is_running = False
        self.finished.emit()