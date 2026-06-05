from PySide6.QtWidgets import (
    QWidget,
    QScrollArea,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLabel
)

from PySide6.QtGui import (
    QFont
)

from src.chronica.ui.resources import (
    QIcons,
    Stylesheets
)

from src.chronica.ui.widgets.common import PlainIconHeader
from src.chronica.ui.widgets.top_apps_item_widget import TopAppsItemWidget
from src.chronica.ui.presentation.models import TopAppsItemData
from src.chronica.ui.styles.style_loader import load_stylesheet

from collections.abc import Iterable

class TopAppsView(QFrame):
    def __init__(self, item_count: int, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("topAppsView")
        self.items: tuple[TopAppsItemWidget, ...] = tuple(
            TopAppsItemWidget(_ + 1,TopAppsItemData.EMPTY_ITEM) for _ in range(item_count)
        )
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        self.header = PlainIconHeader(
            icon=QIcons.get("trophy.png"),
            title="Top Apps",
            icon_w=24,
            icon_h=24,
            title_px=18
        )
        
        self.item_container = QWidget()
        self.item_container.setObjectName("topAppsItemContainer")
        self.container_layout = QVBoxLayout(self.item_container)
        self.container_layout.setContentsMargins(3, 0, 3, 0)
        self.container_layout.setSpacing(5)
        
        # Add placeholder items to the container layout
        for item in self.items:
            self.container_layout.addWidget(item)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("topAppsScrollArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.item_container)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        outer = QWidget()
        outer.setObjectName("topAppsItemContainerOuter")
        outer_layout = QHBoxLayout(outer)
        outer_layout.setContentsMargins(5, 5, 5, 5)
        outer_layout.addWidget(self.scroll_area)
        
        layout.addWidget(self.header)
        layout.addWidget(outer)
        
        self.setStyleSheet(Stylesheets.load("top_apps_view.qss"))
    
    def set_items_data(self, items_data: Iterable[TopAppsItemData]) -> None:
        if len(items_data) > len(self.items):
            raise ValueError(f"Expected smaller or equal to {len(self.items)} items, but got {len(items_data)}.")
        
        for item_widget, item_data in zip(self.items, items_data):
            item_widget.set_data(item_data)