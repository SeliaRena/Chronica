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
from src.chronica.ui.presentation.interpreters.session_history_interpreter import SessionHistoryInterpreter
from src.chronica.ui.styles.style_loader import load_stylesheet
from src.chronica.common.runtime import AppRuntimeContext

class TrackingArchivePanel(QFrame):
    def __init__(self, app_ctx: AppRuntimeContext, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("trackingArchivePanel")
        self.app_ctx = app_ctx
        self.interpreter = SessionHistoryInterpreter(app_ctx.ts_ctx_provider, app_ctx.session_timeline_settings)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        self.tracking_record_selector = TrackingRecordSelector(self.app_ctx)
        self.tracking_record_selector.list_widget.currentItemChanged.connect(self._on_current_record_changed)
        self.tracking_record_viewer = TrackingRecordViewer(self.app_ctx)

        layout.addWidget(self.tracking_record_selector, 1)
        layout.addWidget(self.tracking_record_viewer, 3)

        self.setStyleSheet(load_stylesheet("tracking_archive_panel"))

    def _on_current_record_changed(self, current: QListWidgetItem | None, previous: QListWidgetItem | None):
        report_treeview = self.tracking_record_viewer.report_treeview
        session_timeline_view = self.tracking_record_viewer.session_timeline
        
        if current is None:
            report_treeview.tree_widget.clear()
            return

        item_widget = self.tracking_record_selector.list_widget.itemWidget(current)

        if not isinstance(item_widget, TrackingRecordItemWidget):
            report_treeview.tree_widget.clear()
            return

        tracking_record = item_widget.record
        report_treeview.set_report(tracking_record.app_usage_report)
        session_timeline_view.set_timeline(self.interpreter.to_session_timeline(tracking_record.session_history))