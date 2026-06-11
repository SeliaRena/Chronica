from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QVBoxLayout
)

from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from src.chronica.ui.resources import (
    Stylesheets,
    QIcons
)

from src.chronica.ui.widgets.common import (
    PlainIconHeader
)

from src.chronica.ui.styles.style_loader import load_stylesheet
from src.chronica.ui.widgets.tracking_record_item_widget import TrackingRecordItemWidget
from src.chronica.ui.widgets.tracking_record_filter_bar import TrackingRecordFilterBar
from src.chronica.ui.presentation.models import TrackingRecordDisplay
from src.chronica.storage.sqlite.query import TrackingRecordQuery
from src.chronica.common.runtime import AppRuntimeContext

from src.chronica.characters.character import Character

class TrackingRecordSelector(QFrame):
    def __init__(self, app_ctx: AppRuntimeContext, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("trackingRecordSelector")
        self.app_ctx = app_ctx
        self.chronica: Character | None = None
        
        self.filter_bar = TrackingRecordFilterBar(self)
        self.filter_bar.query_applied.connect(self._on_query_applied)
        
        self.record_list_header = PlainIconHeader(
            QIcons.get("folder.png"),
            "Selected Tracking Records",
            icon_w=24,
            icon_h=24,
            title_px=12,
        )

        self.list_widget = QListWidget(self)
        self.list_widget.setObjectName("selectorListWidget")
        self.list_widget.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        self.list_widget.setTextElideMode(Qt.TextElideMode.ElideRight)
        self.list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)
        
        list_wrapper = QFrame()
        list_wrapper.setObjectName("selectorListWrapper")
        
        wrapper_layout = QVBoxLayout(list_wrapper)
        wrapper_layout.setContentsMargins(10, 10, 10, 10)
        wrapper_layout.addWidget(self.list_widget)
        
        self.record_list = QFrame()
        self.record_list.setObjectName("selectorRecordList")
        self.record_list.setFrameShape(QFrame.Shape.NoFrame)
        
        record_list_layout = QVBoxLayout(self.record_list)
        record_list_layout.setContentsMargins(12, 12, 12, 12)
        record_list_layout.setSpacing(12)
        record_list_layout.addWidget(self.record_list_header)
        record_list_layout.addWidget(list_wrapper)

        layout = QVBoxLayout(self)
        layout.addWidget(self.filter_bar)
        layout.addWidget(self.record_list)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        self.setStyleSheet(load_stylesheet("tracking_record_selector"))
    
    def set_character(self, character: Character) -> None:
        self.chronica = character
        
    def add_tracking_record_item(self, record: TrackingRecordDisplay) -> None:
        item = QListWidgetItem(self.list_widget)
        widget = TrackingRecordItemWidget(record, self.chronica)
        widget.delete_record_requested.connect(self._on_delete_record_requested)

        hint = widget.sizeHint()
        hint.setHeight(hint.height() + 10)
        hint.setWidth(self.list_widget.width() - 20)
        item.setSizeHint(hint)

        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, widget)
    
    def _find_record_specific(self, record_item: TrackingRecordItemWidget) -> QListWidgetItem | None:
        for row in range(self.list_widget.count()):
            item = self.list_widget.item(row)
            
            if self.list_widget.itemWidget(item) is record_item:
                return item
        
        return None

    def _on_query_applied(self, query: TrackingRecordQuery) -> None:
        tracking_records = self.app_ctx.storage.tracking_records
        ts_ctx = self.app_ctx.ts_ctx_provider.get()
        query_result = tracking_records.get_by_query(query)
        
        self.list_widget.clear()
        for record in query_result:
            self.add_tracking_record_item(TrackingRecordDisplay.from_tracking_record(record, ts_ctx))

    def _on_delete_record_requested(self, record_title: str, record_item: TrackingRecordItemWidget) -> None:
        list_item = self._find_record_specific(record_item)
        
        if list_item is None:
            return
        
        row = self.list_widget.row(list_item)
        self.list_widget.removeItemWidget(list_item)
        removed_item = self.list_widget.takeItem(row)
        
        record_item.deleteLater()
        del removed_item
        
        tracking_records = self.app_ctx.storage.tracking_records
        tracking_records.delete_by_title(record_title)
        
        print(f"Deleted {record_title}")