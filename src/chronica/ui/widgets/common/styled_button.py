from PySide6.QtWidgets import (
    QPushButton,
    QWidget
)

from PySide6.QtCore import Qt

from src.chronica.ui.resources import (
    Stylesheets
)

class StyledButton(QPushButton):
    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName("styledButton")
        
        self.setStyleSheet(Stylesheets.load("common", "styled_button.qss"))