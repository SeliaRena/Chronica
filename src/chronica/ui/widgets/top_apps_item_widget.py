from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QProgressBar,
    QSizePolicy
)

from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt

from src.chronica.ui.resources import (
    Stylesheets,
    QIcons,
    AppIconProvider
)

from src.chronica.ui.widgets.common.factories import (
    icon_label,
    container
)

from src.chronica.ui.presentation.models import TopAppsItemData
from src.chronica.ui.widgets.elided_label import ElidedLabel

def fallback_icon() -> QIcon:
    return QIcons.get("uniqueness.png")

def placement_icon(placement: int) -> QIcon | None:
    match placement:
        case 1:
            return QIcons.get("vip.png")
        case 2:
            return QIcons.get("2nd-place.png")
        case 3:
            return QIcons.get("3rd-place.png")
        case _:
            return None

def placement_icon_or_placeholder(placement: int) -> QLabel:
    icon = placement_icon(placement)
    
    if icon is not None:
        return icon_label(
            icon,
            w=18,
            h=18,
            object_name="topAppsItemPlacementIconLabel"
        )
    else:
        placeholder = QLabel("")
        placeholder.setObjectName("topAppsItemPlacementIconLabel")
        placeholder.setFixedSize(18, 18)
        
        return placeholder

def percentage(ratio: float) -> int:
    return int(ratio * 100)

class TopAppsItemWidget(QFrame):
    def __init__(self, placement: int, data: TopAppsItemData, parent: QWidget | None = None):
        super().__init__(parent)
        self.placement = placement
        self.data = data
        self.setObjectName("topAppsItemWidget")
        self.setFrameShape(QFrame.Shape.NoFrame)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(8)
        
        self.placement_icon_label = placement_icon_or_placeholder(self.placement)
        self.app_icon_label = icon_label(
            fallback_icon(),
            w=24,
            h=24,
            object_name="topAppsItemIconLabel"
        )
        
        self.right_content, right_content_layout = container(
            host=QFrame(frameShape=QFrame.Shape.NoFrame),
            host_object_name="topAppsItemRightContent",
            vertical=True,
            margins=(0, 0, 0, 0),
            spacing=5
        )
        
        self.stats, stats_layout = container(
            host=QFrame(frameShape=QFrame.Shape.NoFrame),
            host_object_name="topAppsItemStats",
            vertical=False,
            margins=(0, 0, 0, 0),
            spacing=0
        )
        
        self.app_name_label = ElidedLabel("")
        self.app_name_label.setObjectName("topAppsItemAppNameLabel")
        self.app_name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.bar_percentage_label = ElidedLabel("")
        self.bar_percentage_label.setObjectName("topAppsItemBarPercentageLabel")
        self.bar_percentage_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        stats_layout.addWidget(self.app_name_label)
        stats_layout.addWidget(self.bar_percentage_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("topAppsItemProgressBar")
        self.progress_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        
        self.duration_label = ElidedLabel("")
        self.duration_label.setObjectName("topAppsItemDurationLabel")
        
        right_content_layout.addWidget(self.stats)
        right_content_layout.addWidget(self.progress_bar)
        right_content_layout.addWidget(self.duration_label)
        
        layout.addWidget(self.placement_icon_label, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.app_icon_label, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.right_content)
        
        self.set_data(data)
        self.setStyleSheet(Stylesheets.load("top_apps_item_widget.qss"))
        
    def set_data(self, data: TopAppsItemData) -> None:
        app_icon = fallback_icon()
        self.app_icon_label.setPixmap(app_icon.pixmap(24, 24))
        self.app_name_label.setText(data.app_name)
        self.bar_percentage_label.setText(f"{percentage(data.bar_ratio)}%")
        self.progress_bar.setValue(percentage(data.bar_ratio))
        self.duration_label.setText(data.duration)
        self.data = data