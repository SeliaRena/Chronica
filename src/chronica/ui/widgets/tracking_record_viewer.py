from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QFrame
)

from src.chronica.ui.widgets.common import (
    PlainIconHeader,
    StyledButton
)

from src.chronica.ui.resources import (
    Stylesheets,
    QIcons
)

from src.chronica.ui.styles.style_loader import load_stylesheet
from src.chronica.ui.widgets.app_usage_report_treeview import AppUsageReportTreeview
from src.chronica.ui.widgets.usage_report import UsageReportView
from src.chronica.ui.widgets.session_timeline_view import SessionTimelineView
from src.chronica.common.runtime import AppRuntimeContext

class TrackingRecordViewer(QFrame):
    def __init__(self, app_ctx: AppRuntimeContext, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("trackingRecordViewer")
        self.app_ctx = app_ctx
        
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(12)
        
        # 1. view mode bar
        self.view_mode_bar = self._build_view_mode_bar()
        self.view_mode_bar.setObjectName("viewModeBar")
        
        # 2. display section
        self.usage_report = UsageReportView(app_ctx.app_icon_provider) # index 0
        self.session_timeline = SessionTimelineView(self.app_ctx.ts_ctx_provider.get()) # index 1
        
        timeline_area = QFrame(frameShape=QFrame.Shape.NoFrame)
        timeline_area.setObjectName("sessionTimelineArea")
        timeline_layout = QVBoxLayout(timeline_area)
        timeline_layout.setContentsMargins(14, 14, 14, 14)
        timeline_layout.setSpacing(12)
        
        timeline_header = PlainIconHeader(
            QIcons.get("video-editing.png"),
            "Activity Timeline",
            icon_w=24,
            icon_h=24,
            title_px=12,
        )
        quick_container = QWidget.createWindowContainer(self.session_timeline)
        
        timeline_layout.addWidget(timeline_header, 0)
        timeline_layout.addWidget(quick_container, 1)
        
        self.display_section_stack = QStackedWidget()
        self.display_section_stack.addWidget(self.usage_report)
        self.display_section_stack.addWidget(timeline_area)
        
        # 3. integration
        root_layout.addWidget(self.view_mode_bar)
        root_layout.addWidget(self.display_section_stack)
        
        # 4. initialization
        self._connect_view_mode_bar_buttons()
        self.switch_to_usage_report()
        
        # 5. style
        self.setStyleSheet(load_stylesheet("tracking_record_viewer"))
        
    def _build_view_mode_bar(self) -> QWidget:
        view_mode_bar = QWidget()
        view_mode_buttons = QWidget()
        
        layout = QHBoxLayout(view_mode_buttons)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        self.bar_header = PlainIconHeader(
            QIcons.load("dashboard.png"),
            "Views",
            icon_w=24,
            icon_h=24,
            title_px=12
        )
        
        self.show_app_usage_report_button = StyledButton("Show Usage Report")
        self.show_session_timeline_button = StyledButton("Show Activity Timeline")
        
        layout.addWidget(self.show_app_usage_report_button, 0)
        layout.addWidget(self.show_session_timeline_button, 0)
        layout.addStretch()
        
        bar_layout = QVBoxLayout(view_mode_bar)
        bar_layout.setContentsMargins(12, 12, 12, 12)
        bar_layout.setSpacing(12)
        bar_layout.addWidget(self.bar_header)
        bar_layout.addWidget(view_mode_buttons)
        
        return view_mode_bar
    
    def _connect_view_mode_bar_buttons(self) -> None:
        self.show_app_usage_report_button.clicked.connect(self.switch_to_usage_report)
        self.show_session_timeline_button.clicked.connect(self.switch_to_session_timeline)
    
    def set_active_button(self, button_name: str) -> None:
        buttons = {
            "showAppUsageReportButton": self.show_app_usage_report_button,
            "showSessionTimelineButton": self.show_session_timeline_button
        }
        
        for key, button in buttons.items():
            button.setProperty("active", key == button_name)
            button.style().unpolish(button)
            button.style().polish(button)
            button.update()
            
    def switch_to_usage_report(self) -> None:
        self.display_section_stack.setCurrentIndex(0)
        # self.set_active_button("showAppUsageReportButton")
        
    def switch_to_session_timeline(self) -> None:
        self.display_section_stack.setCurrentIndex(1)
        # self.set_active_button("showSessionTimelineButton")