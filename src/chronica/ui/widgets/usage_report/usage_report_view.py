from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFrame,
    QScrollArea,
    QSizePolicy,
    QLabel
)

from src.chronica.ui.resources import (
    AppIconProvider
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

        self.title_label = QLabel("Usage Report")
        self.title_label.setObjectName("reportViewTitleLabel")
        self.title_label.setWordWrap(True)

        self.usage_report_widget = QWidget()
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("usageReportScrollArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.usage_report_widget)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.scroll_area)
    
    def set_report(self, report_data: UsageReportData) -> None:
        self.usage_report_widget = UsageReportWidget(report_data, self.app_icon_provider)
        self.scroll_area.setWidget(self.usage_report_widget)
        
    def clear(self) -> None:
        self.usage_report_widget = QWidget()
        self.scroll_area.setWidget(self.usage_report_widget)