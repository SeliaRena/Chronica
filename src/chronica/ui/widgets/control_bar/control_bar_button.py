from PySide6.QtWidgets import (
    QPushButton,
    QWidget
)

from PySide6.QtCore import Qt, QSize

from PySide6.QtGui import QIcon

from src.chronica.ui.resources import (
    Stylesheets
)

class ControlBarButton(QPushButton):
    def __init__(
        self,
        text: str,
        *,
        icon: QIcon | None = None,
        icon_size: int | None = None,
        parent: QWidget | None = None
    ) -> None:
        super().__init__(text, parent)
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName("controlBarButton")
        
        if icon is not None:
            self.setIcon(icon)
        
        if icon_size is not None:
            self.setIconSize(QSize(icon_size, icon_size))
        
        self.setStyleSheet(Stylesheets.load("control_bar", "control_bar_button.qss"))