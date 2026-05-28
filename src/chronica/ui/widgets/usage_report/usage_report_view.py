from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFrame,
    QScrollArea,
    QSizePolicy,
    QLabel
)

from src.chronica.ui.resources import (
    Stylesheets,
    AppIconProvider,
    QIcons
)

from src.chronica.ui.widgets.common import (
    PlainIconHeader
)

from src.chronica.ui.widgets.usage_report.usage_report_widget import UsageReportWidget
from src.chronica.ui.presentation.models import UsageReportData

class UsageReportView(QFrame):
    def __init__(self, app_icon_provider: AppIconProvider, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("usageReportView")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.app_icon_provider = app_icon_provider

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        self.header = PlainIconHeader(
            QIcons.load("data-analytics.png"),
            "Usage Report",
            icon_w=28,
            icon_h=28,
            title_px=14,
        )

        self.usage_report_widget = self._default_widget()
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("usageReportScrollArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.usage_report_widget)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        self.scroll_area_frame = QFrame()
        self.scroll_area_frame.setObjectName("usageReportScrollAreaFrame")
        self.scroll_area_frame.setFrameShape(QFrame.Shape.NoFrame)

        frame_layout = QVBoxLayout(self.scroll_area_frame)
        frame_layout.setContentsMargins(3, 3, 3, 3)
        frame_layout.setSpacing(0)
        frame_layout.addWidget(self.scroll_area)
        
        layout.addWidget(self.header)
        layout.addWidget(self.scroll_area_frame)
        
        self.setStyleSheet(Stylesheets.load("usage_report", "usage_report_view.qss"))
    
    def set_report(self, report_data: UsageReportData) -> None:
        self.usage_report_widget = UsageReportWidget(report_data, self.app_icon_provider)
        self.scroll_area.setWidget(self.usage_report_widget)
        
    def clear(self) -> None:
        self.usage_report_widget = self._default_widget()
        self.scroll_area.setWidget(self.usage_report_widget)
    
    def _default_widget(self) -> QWidget:
        widget = QWidget()
        widget.setStyleSheet("QWidget { background-color: transparent; }")
        return widget