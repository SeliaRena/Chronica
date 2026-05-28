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
    QSS
)

class IconHeader(QFrame):
    def __init__(
        self, 
        icon: QIcon, 
        title: str,
        subtitle: str,
        *,
        icon_size: QSize = QSize(32, 32),
        title_px: int = 14,
        title_bold: bool = True,
        title_italic: bool = False,
        subtitle_px: int = 10,
        subtitle_bold: bool = False,
        subtitle_italic: bool = True,
        custom_title_font: QFont | None = None,
        custom_subtitle_font: QFont | None = None,
        parent: QWidget | None = None
    ):
        super().__init__(parent)
        self.setObjectName("iconHeader")
        self.setFrameShape(QFrame.StyledPanel)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)
        
        self.icon_label = QLabel()
        self.icon_label.setObjectName("iconHeaderIconLabel")
        self.icon_label.setScaledContents(True)
        self.icon_label.setFixedSize(icon_size)
        self.icon_label.setPixmap(icon.pixmap(icon_size))
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.icon_box = QFrame()
        self.icon_box.setObjectName("iconHeaderIconBox")
        self.icon_box.setFrameShape(QFrame.StyledPanel)
        self.icon_box.setFrameShadow(QFrame.Shadow.Raised)
        self.icon_box.setFixedSize(QSize(icon_size.width() + 18, icon_size.height() + 18))
        
        box_layout = QVBoxLayout(self.icon_box)
        box_layout.setContentsMargins(0, 0, 0, 0)
        box_layout.setSpacing(0)
        box_layout.addWidget(self.icon_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        right_content = QVBoxLayout()
        
        self.title_label = QLabel(title)
        self.title_label.setObjectName("iconHeaderTitleLabel")
        self.title_label.setWordWrap(True)
        if custom_title_font is not None:
            self.title_label.setFont(custom_title_font)
        
        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setObjectName("iconHeaderSubtitleLabel")
        self.subtitle_label.setWordWrap(True)
        if custom_subtitle_font is not None:
            self.subtitle_label.setFont(custom_subtitle_font)
        
        right_content.addWidget(self.title_label)
        right_content.addWidget(self.subtitle_label)
        
        layout.addWidget(self.icon_box)
        layout.addLayout(right_content)
        
        title_font_weight = QSS.Value.FontWeight.BOLD if title_bold else None
        title_font_style = QSS.Value.FontStyle.ITALIC if title_italic else None
        subtitle_font_weight = QSS.Value.FontWeight.BOLD if subtitle_bold else None
        subtitle_font_style = QSS.Value.FontStyle.ITALIC if subtitle_italic else None
        
        self.setStyleSheet(
            Stylesheets.load(
                "common",
                "icon_header.qss",
                title_font_size=title_px,
                title_font_weight=QSS.PropertyLine.font_weight(title_font_weight),
                title_font_style=QSS.PropertyLine.font_style(title_font_style),
                subtitle_font_size=subtitle_px,
                subtitle_font_weight=QSS.PropertyLine.font_weight(subtitle_font_weight),
                subtitle_font_style=QSS.PropertyLine.font_style(subtitle_font_style)
            )
        )