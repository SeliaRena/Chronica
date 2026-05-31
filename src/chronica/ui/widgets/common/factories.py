from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLayout
)

from PySide6.QtCore import (
    Qt,
    QSize
)

from PySide6.QtGui import (
    QIcon
)

type ContentMargins = tuple[int, int, int, int]
type HostAndLayout = tuple[QWidget, QLayout]

def icon_button(
    icon: QIcon,
    *,
    button_size: int = 32,
    icon_size: int = 24,
    object_name: str | None = None,
    tooltip: str | None = None
) -> QPushButton:
    button = QPushButton()
    button.setIcon(icon)
    button.setIconSize(QSize(icon_size, icon_size))
    button.setFixedSize(button_size, button_size)
    button.setCursor(Qt.CursorShape.PointingHandCursor)

    if object_name is not None:
        button.setObjectName(object_name)

    if tooltip is not None:
        button.setToolTip(tooltip)

    return button

def container(
    host: QWidget,
    *,
    host_object_name: str | None = None,
    vertical: bool = True,
    margins: ContentMargins = (0, 0, 0, 0),
    spacing: int = 0
) -> HostAndLayout:
    if host_object_name is not None:
        host.setObjectName(host_object_name)

    layout = QVBoxLayout(host) if vertical else QHBoxLayout(host)
    layout.setContentsMargins(*margins)
    layout.setSpacing(spacing)
    
    return host, layout