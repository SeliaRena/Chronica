from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QVBoxLayout,
    QTreeWidget,
    QTreeWidgetItem,
    QAbstractItemView,
    QHeaderView
)
from PySide6.QtCore import Qt

from src.chronica.domain.app_usage_report import AppUsageReport
from src.chronica.ui.styles.style_loader import load_stylesheet
from src.chronica.ui.presentation.models import ReportNode, ReportNodeMapper
from src.chronica.common.app_runtime_context import AppRuntimeContext

class TrackingRecordViewer(QFrame):
    def __init__(self, app_ctx: AppRuntimeContext, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("trackingRecordViewer")
        self.app_ctx = app_ctx
        self.node_mapper = ReportNodeMapper(self.app_ctx.ts_ctx_provider)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setColumnCount(3)
        self.tree_widget.setHeaderLabels(["Name", "Duration", "Detail"])
        self.tree_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.tree_widget.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.tree_widget.setIndentation(16)
        
        header = self.tree_widget.header()
        # header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        tree_wrapper = QWidget()
        tree_wrapper.setObjectName("treeWrapper")
        wrapper_layout = QVBoxLayout(tree_wrapper)
        wrapper_layout.setContentsMargins(5, 5, 5, 5)
        wrapper_layout.addWidget(self.tree_widget, 1)
        
        layout.addWidget(tree_wrapper)
        
        self.setStyleSheet(load_stylesheet("tracking_record_viewer"))

    def _make_tree_item(self, node: ReportNode) -> QTreeWidgetItem:
        item = QTreeWidgetItem([node.name, node.duration, node.detail])
        item.setData(0, Qt.ItemDataRole.UserRole, node)
        
        for childnode in node.children:
            item.addChild(self._make_tree_item(childnode))
        
        return item
    
    def _apply_item_properties(self, item: QTreeWidgetItem) -> None:
        report_node: ReportNode = item.data(0, Qt.ItemDataRole.UserRole)
        
        if report_node.tooltip:
            item.setToolTip(0, report_node.tooltip)
            item.setToolTip(2, report_node.tooltip)
        item.setExpanded(report_node.default_expanded)
        
        for i in range(item.childCount()):
            self._apply_item_properties(item.child(i))

    def set_report(self, report: AppUsageReport) -> None:
        top_level_item = self._make_tree_item(self.node_mapper.from_app_usage_report(report))
        
        self.tree_widget.clear()
        self.tree_widget.addTopLevelItem(top_level_item)
        self._apply_item_properties(top_level_item)
        self.tree_widget.resizeColumnToContents(0)
        self.tree_widget.resizeColumnToContents(2)