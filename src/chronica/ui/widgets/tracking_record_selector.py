from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QVBoxLayout
)
from PySide6.QtGui import QFont

from src.chronica.ui.styles.style_loader import load_stylesheet
from src.chronica.ui.widgets.tracking_record_item_widget import TrackingRecordItemWidget
from src.chronica.ui.widgets.tracking_record_filter_bar import TrackingRecordFilterBar
from src.chronica.ui.presentation.models import TrackingRecordDisplay
from src.chronica.storage.sqlite.query import TrackingRecordQuery
from src.chronica.common.runtime import AppRuntimeContext

class TrackingRecordSelector(QFrame):
    def __init__(self, app_ctx: AppRuntimeContext, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("trackingRecordSelector")
        self.app_ctx = app_ctx
        
        title_label = QLabel("Selected Records")
        title_label.setObjectName("titleLabel")
        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        self.filter_bar = TrackingRecordFilterBar(self)
        self.filter_bar.query_applied.connect(self._on_query_applied)

        self.list_widget = QListWidget(self)
        self.list_widget.setObjectName("selectorListWidget")
        list_wrapper = QFrame()
        list_wrapper.setObjectName("selectorListWrapper")
        wrapper_layout = QVBoxLayout(list_wrapper)
        wrapper_layout.setContentsMargins(5, 5, 5, 5)
        wrapper_layout.addWidget(self.list_widget, 1)

        layout = QVBoxLayout(self)
        layout.addWidget(self.filter_bar)
        layout.addWidget(title_label)
        layout.addWidget(list_wrapper)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        self.setStyleSheet(load_stylesheet("tracking_record_selector"))
        
    def add_tracking_record_item(self, record: TrackingRecordDisplay) -> None:
        item = QListWidgetItem(self.list_widget)
        widget = TrackingRecordItemWidget(record)

        item.setSizeHint(widget.sizeHint())

        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, widget)

    def _on_query_applied(self, query: TrackingRecordQuery) -> None:
        tracking_records = self.app_ctx.storage.tracking_records
        ts_ctx = self.app_ctx.ts_ctx_provider.get()
        query_result = tracking_records.get_by_query(query)
        
        self.list_widget.clear()
        for record in query_result:
            self.add_tracking_record_item(TrackingRecordDisplay.from_tracking_record(record, ts_ctx))