from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QHBoxLayout,
    QStackedWidget,
    QListWidgetItem
)

from src.chronica.ui.widgets.tracking_record_selector import TrackingRecordSelector
from src.chronica.ui.widgets.tracking_record_item_widget import TrackingRecordItemWidget
from src.chronica.ui.widgets.tracking_record_viewer import TrackingRecordViewer
from src.chronica.ui.styles.style_loader import load_stylesheet

class TrackingArchivePanel(QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("trackingArchivePanel")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)
        
        self.tracking_record_selector = TrackingRecordSelector()
        self.tracking_record_selector.list_widget.currentItemChanged.connect(self._on_current_record_changed)
        self.tracking_record_viewer = TrackingRecordViewer()

        layout.addWidget(self.tracking_record_selector, 1)
        layout.addWidget(self.tracking_record_viewer, 3)
        
        self.setStyleSheet(load_stylesheet("tracking_archive_panel"))
        
    def _on_current_record_changed(self, current: QListWidgetItem | None, previous: QListWidgetItem | None):
        if current is None:
            self.tracking_record_viewer.tree_widget.clear()
            return

        widget = self.tracking_record_selector.list_widget.itemWidget(current)

        if not isinstance(widget, TrackingRecordItemWidget):
            self.tracking_record_viewer.tree_widget.clear()
            return
        
        record = widget.tracking_record
        self.tracking_record_viewer.set_report(record.app_usage_report)