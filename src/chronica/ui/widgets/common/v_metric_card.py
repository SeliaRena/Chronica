from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame
)

from PySide6.QtGui import (
    QFont
)

from PySide6.QtCore import Qt

from src.chronica.ui.resources import (
    Stylesheets
)

from src.chronica.ui.widgets.elided_label import ElidedLabel

class VMetricCard(QFrame):
    def __init__(self, title: str, value: str, *, value_font_px: int = 20, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("vMetricCard")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setAutoFillBackground(False)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(7, 7, 7, 7)
        layout.setSpacing(7)
        
        self.title_label = ElidedLabel(title)
        self.title_label.setObjectName("vMetricCardTitleLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setToolTip(title)
        
        self.value_label = ElidedLabel(value)
        self.value_label.setObjectName("vMetricCardValueLabel")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label.setToolTip(value)

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)

        self.setStyleSheet(
            Stylesheets.load(
                "common",
                "v_metric_card.qss",
                font_size=value_font_px
            )
        )