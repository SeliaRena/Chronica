from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QProgressBar,
    QSizePolicy
)

from PySide6.QtGui import (
    QFont,
    QIcon
)

from PySide6.QtCore import QSize, Qt

from src.chronica.ui.styles.style_loader import load_stylesheet
from src.chronica.ui.presentation.models import TopAppsItemData
from src.chronica.common.resource_locator import ResourceLocator
from src.chronica.ui.widgets.elided_label import ElidedLabel

FALLBACK_ICON_PATH = str(ResourceLocator.ui_icon("app.png"))
def fallback_icon() -> QIcon:
    return QIcon(FALLBACK_ICON_PATH)

class TopAppsItemWidget(QWidget):
    def __init__(self, data: TopAppsItemData, parent: QWidget | None = None):
        super().__init__(parent)
        self.data = data
        self.setObjectName("topAppsItemWidget")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(8)
        
        # structure: widget -> ([app icon] [app name + progress bar] [share ratio] [duration])
        # 1. app icon
        app_icon = QIcon(str(self.data.icon_path)) if self.data.icon_path else fallback_icon()
        self.app_icon_label = QLabel()
        self.app_icon_label.setObjectName("appIconLabel")
        self.app_icon_label.setFixedSize(QSize(24, 24))
        self.app_icon_label.setScaledContents(True)
        self.app_icon_label.setPixmap(app_icon.pixmap(24, 24))
        
        # 2. app name + progress bar
        self.name_and_progress = QWidget()
        self.name_and_progress.setObjectName("nameAndProgress")
        name_and_progress_layout = QHBoxLayout(self.name_and_progress)
        
        self.name_label = ElidedLabel(self.data.app_name)
        self.name_label.setFixedWidth(72)
        self.name_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setMinimumWidth(150)
        self.progress_bar.setFixedHeight(20)
        self.progress_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(int(self.data.bar_ratio * 100.0))
        
        name_and_progress_layout.addWidget(self.name_label)
        name_and_progress_layout.addWidget(self.progress_bar)
        
        # 3. share ratio
        self.share_ratio_label = QLabel(f"{int(self.data.share_ratio * 100)}%")
        self.share_ratio_label.setObjectName("shareRatioLabel")
        self.share_ratio_label.setFixedWidth(48)
        self.share_ratio_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 4. duration
        self.duration_label = ElidedLabel(self.data.duration)
        self.duration_label.setObjectName("durationLabel")
        self.duration_label.setFixedWidth(72)
        self.duration_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # assemble
        layout.addWidget(self.app_icon_label, 0)
        layout.addWidget(self.name_and_progress, 1)
        layout.addWidget(self.share_ratio_label, 0)
        layout.addWidget(self.duration_label, 0)
        
        self.setStyleSheet(load_stylesheet("top_apps_item_widget"))
        
    def set_data(self, data: TopAppsItemData) -> None:
        app_icon = QIcon(str(data.icon_path)) if data.icon_path else fallback_icon()
        self.app_icon_label.setPixmap(app_icon.pixmap(24, 24))
        self.name_label.setText(data.app_name)
        self.progress_bar.setValue(int(data.bar_ratio * 100.0))
        self.share_ratio_label.setText(f"{int(data.share_ratio * 100)}%")
        self.duration_label.setText(data.duration)
        self.data = data