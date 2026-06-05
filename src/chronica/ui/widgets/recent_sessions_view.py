from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QFrame,
    QScrollArea
)

from PySide6.QtGui import (
    QFont
)

from PySide6.QtCore import Qt

from src.chronica.ui.widgets.common import (
    PlainIconHeader
)

from src.chronica.ui.resources import (
    QIcons,
    Stylesheets
)

from src.chronica.ui.widgets.recent_sessions_item_widget import RecentSessionsItemWidget
from src.chronica.ui.presentation.models import RecentSessionsItemData
from src.chronica.ui.styles.style_loader import load_stylesheet

from collections.abc import Iterable

class RecentSessionsView(QFrame):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("recentSessionsView")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        self.header = PlainIconHeader(
            icon=QIcons.get("timeline.png"),
            title="Recent Sessions",
            icon_w=24,
            icon_h=24,
            title_px=18,
        )
        
        self.item_container = QWidget()
        self.item_container.setObjectName("recentSessionsItemContainer")
        self.container_layout = QVBoxLayout(self.item_container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(0)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("recentSessionsScrollArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.item_container)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        recent_sessions_outer = QWidget()
        recent_sessions_outer.setObjectName("recentSessionsOuter")
        outer_layout = QHBoxLayout(recent_sessions_outer)
        outer_layout.setContentsMargins(5, 5, 5, 5)
        outer_layout.addWidget(self.scroll_area)
        
        layout.addWidget(self.header)
        layout.addWidget(recent_sessions_outer)
        
        self.setStyleSheet(load_stylesheet("recent_sessions_view"))
        
    def _clear_container(self) -> None:
        while self.container_layout.count():
            item = self.container_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
        
    def set_recent_sessions(self, data: Iterable[RecentSessionsItemData]) -> None:
        self._clear_container()
        
        for item in reversed(tuple(data)):
            self.container_layout.addWidget(RecentSessionsItemWidget(item))