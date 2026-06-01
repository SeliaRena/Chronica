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

from src.chronica.ui.widgets.common.factories import (
    icon_label
)

from src.chronica.ui.widgets.elided_label import ElidedLabel

class PlainIconHeader(QFrame):
    def __init__(
        self,
        icon: QIcon,
        title: str,
        *,
        icon_w: int = 24,
        icon_h: int = 24,
        title_px: int = 14,
        font_weight: int = 700,
        compress_content_left: bool = False,
        parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)

        self.setObjectName("plainIconHeader")
        self.setFrameShape(QFrame.Shape.NoFrame)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self.icon_label = icon_label(
            icon,
            w=icon_w,
            h=icon_h,
            object_name="plainIconHeaderIconLabel"
        )

        self.title_label = ElidedLabel(title)
        self.title_label.setToolTip(title)
        self.title_label.setObjectName("plainIconHeaderTitleLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        layout.addWidget(self.icon_label, 0, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.title_label, 1, alignment=Qt.AlignmentFlag.AlignVCenter)
        
        if compress_content_left:
            layout.addStretch()
        
        self.setStyleSheet(
            Stylesheets.load(
                "common",
                "plain_icon_header.qss",
                font_size=title_px,
                font_weight=font_weight
            )
        )
    
    def set_title(self, title: str) -> None:
        self.title_label.setText(title)
        self.title_label.setToolTip(title)
    
    def set_icon(self, icon: QIcon, w: int | None = None, h: int | None = None) -> None:
        if w is not None and h is not None:
            self.icon_label.setPixmap(icon.pixmap(QSize(w, h)))
        else:
            self.icon_label.setPixmap(icon.pixmap(self.icon_label.size()))