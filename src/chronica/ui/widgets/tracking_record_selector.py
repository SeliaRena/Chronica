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
from src.chronica.ui.data_display.display_models import TrackingRecordDisplay

class TrackingRecordSelector(QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("trackingRecordSelector")
        
        title_label = QLabel("Selected Records")
        title_label.setObjectName("titleLabel")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)

        self.list_widget = QListWidget(self)
        self.list_widget.setObjectName("selectorListWidget")
        list_wrapper = QFrame()
        list_wrapper.setObjectName("selectorListWrapper")
        wrapper_layout = QVBoxLayout(list_wrapper)
        wrapper_layout.setContentsMargins(5, 5, 5, 5)
        wrapper_layout.addWidget(self.list_widget, 1)

        layout = QVBoxLayout(self)
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