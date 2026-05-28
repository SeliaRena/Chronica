from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QFrame,
    QSizePolicy
)

from PySide6.QtGui import (
    QFont,
    QIcon
)

from PySide6.QtCore import QSize, Qt

from src.chronica.ui.resources import (
    Stylesheets,
    QSS,
    QIcons
)

class PlainIconHeader(QFrame):
    def __init__(
        self,
        icon: QIcon,
        title: str,
        *,
        icon_w: int = 24,
        icon_h: int = 24,
        title_px: int = 14,
        parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)

        self.setObjectName("plainIconHeader")
        self.setFrameShape(QFrame.Shape.NoFrame)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self.icon_label = QIcons.make_icon_label(
            icon,
            w=icon_w,
            h=icon_h,
            object_name="plainIconHeaderIconLabel"
        )

        self.title_label = QLabel(title)
        self.title_label.setObjectName("plainIconHeaderTitleLabel")
        self.title_label.setWordWrap(True)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        layout.addWidget(self.icon_label, 0, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.title_label, 0, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addStretch()
        
        self.setStyleSheet(
            Stylesheets.load(
                "common",
                "plain_icon_header.qss",
                font_size=title_px
            )
        )