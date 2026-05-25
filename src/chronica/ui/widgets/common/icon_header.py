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

from PySide6.QtCore import QSize

class IconHeader(QFrame):
    def __init__(
        self, 
        icon: QIcon, 
        title: str, 
        subtitle: str, 
        *,
        icon_size: QSize = QSize(24, 24),
        title_size: int = 12,
        title_bold: bool = True,
        title_italic: bool = False,
        subtitle_size: int = 10,
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
        
        self.icon_label = QLabel()
        self.icon_label.setObjectName("iconLabel")
        self.icon_label.setScaledContents(True)
        self.icon_label.setFixedSize(icon_size)
        self.icon_label.setPixmap(icon.pixmap(icon_size))
        
        right_content = QVBoxLayout()
        
        self.title_label = QLabel(title)
        self.title_label.setObjectName("titleLabel")
        self.title_label.setWordWrap(True)
        self._init_font(self.title_label, title_size, title_bold, title_italic, custom_title_font)
        
        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setObjectName("subtitleLabel")
        self.subtitle_label.setWordWrap(True)
        self._init_font(self.subtitle_label, subtitle_size, subtitle_bold, subtitle_italic, custom_subtitle_font)
        
        right_content.addWidget(self.title_label)
        right_content.addWidget(self.subtitle_label)
        
        layout.addWidget(self.icon_label)
        layout.addLayout(right_content)
        
    def _init_font(self, label: QLabel, size: int, bold: bool, italic: bool, custom_font: QFont | None = None) -> None:
        if custom_font:
            label.setFont(custom_font)
        else:
            font = QFont()
            font.setPointSize(size)
            font.setBold(bold)
            font.setItalic(italic)
            label.setFont(font)