from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import QLabel

class ElidedLabel(QLabel):
    def __init__(
        self,
        text: str = "",
        mode: Qt.TextElideMode = Qt.TextElideMode.ElideRight,
        parent=None,
    ):
        super().__init__(parent)

        self._full_text = text
        self._mode = mode

        self.setToolTip(text)
        self._update_elided_text()

    def setText(self, text: str) -> None:
        self._full_text = text
        self.setToolTip(text)
        self._update_elided_text()

    def fullText(self) -> str:
        return self._full_text

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._update_elided_text()

    def _update_elided_text(self) -> None:
        metrics = QFontMetrics(self.font())

        elided = metrics.elidedText(
            self._full_text,
            self._mode,
            max(0, self.width() - 4),
        )

        super().setText(elided)