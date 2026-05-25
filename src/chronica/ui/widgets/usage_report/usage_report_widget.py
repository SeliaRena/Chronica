from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFrame
)

from src.chronica.ui.resources import (
    Stylesheets,
    AppIconProvider
)

from src.chronica.ui.presentation.models import (
    AppUsageItemData,
    UsageReportData
)

from src.chronica.ui.widgets.usage_report.app_usage_item_widget import AppUsageItemWidget

class UsageReportWidget(QFrame):
    def __init__(self, data: UsageReportData, app_icon_provider: AppIconProvider, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("usageReportWidget")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.data = data
        self.app_icon_provider = app_icon_provider

        layout = QVBoxLayout(self)

        for app_item_data in self.data.apps:
            layout.addWidget(AppUsageItemWidget(app_item_data, self.app_icon_provider))