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
from src.chronica.common.app_runtime_context import AppRuntimeContext

class TrackingArchivePanel(QFrame):
    def __init__(self, app_ctx: AppRuntimeContext, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("trackingArchivePanel")
        self.app_ctx = app_ctx

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        self.tracking_record_selector = TrackingRecordSelector()
        self.tracking_record_selector.list_widget.currentItemChanged.connect(self._on_current_record_changed)
        self.tracking_record_viewer = TrackingRecordViewer(self.app_ctx)

        layout.addWidget(self.tracking_record_selector, 1)
        layout.addWidget(self.tracking_record_viewer, 3)

        self.setStyleSheet(load_stylesheet("tracking_archive_panel"))

    def _on_current_record_changed(self, current: QListWidgetItem | None, previous: QListWidgetItem | None):
        if current is None:
            self.tracking_record_viewer.tree_widget.clear()
            return

        item_widget = self.tracking_record_selector.list_widget.itemWidget(current)

        if not isinstance(item_widget, TrackingRecordItemWidget):
            self.tracking_record_viewer.tree_widget.clear()
            return

        self.tracking_record_viewer.set_report(item_widget.record.app_usage_report)