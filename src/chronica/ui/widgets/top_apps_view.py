from PySide6.QtWidgets import (
    QWidget,
    QScrollArea,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLabel
)

from src.chronica.ui.widgets.top_apps_item_widget import TopAppsItemWidget
from src.chronica.ui.presentation.models import TopAppsItemData

from collections.abc import Iterable

class TopAppsView(QFrame):
    def __init__(self, item_count: int, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("topAppsView")
        self.items: tuple[TopAppsItemWidget, ...] = tuple(
            TopAppsItemWidget(TopAppsItemData.EMPTY_ITEM) for _ in range(item_count)
        )
        
        layout = QVBoxLayout(self)
        
        title_label = QLabel("Top Apps")
        
        self.item_container = QWidget()
        self.container_layout = QVBoxLayout(self.item_container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(8)
        
        # Add placeholder items to the container layout
        for item in self.items:
            self.container_layout.addWidget(item)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.item_container)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        layout.addWidget(title_label)
        layout.addWidget(self.scroll_area)
    
    def set_items_data(self, items_data: Iterable[TopAppsItemData]) -> None:
        if len(items_data) > len(self.items):
            raise ValueError(f"Expected smaller or equal to {len(self.items)} items, but got {len(items_data)}.")
        
        for item_widget, item_data in zip(self.items, items_data):
            item_widget.set_data(item_data)