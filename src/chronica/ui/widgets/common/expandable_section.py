from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QToolButton,
    QSizePolicy,
)

from src.chronica.ui.resources import (
    Stylesheets,
)

class ExpandableSection(QFrame):
    toggled = Signal(bool)

    def __init__(
        self,
        title: str,
        content: QWidget | None = None,
        *,
        initially_expanded: bool = True,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)

        self._expanded = initially_expanded

        self.setObjectName("ExpandableSection")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)

        self._toggle_button = QToolButton()
        self._toggle_button.setObjectName("ExpandableSectionToggleButton")
        self._toggle_button.setAutoRaise(True)
        self._toggle_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._toggle_button.clicked.connect(self.toggle)

        self._title_label = QLabel(title)
        self._title_label.setObjectName("ExpandableSectionTitle")

        self._header = QWidget()
        self._header.setObjectName("ExpandableSectionHeader")
        self._header.setCursor(Qt.CursorShape.PointingHandCursor)
        self._header.mousePressEvent = self._on_header_pressed

        header_layout = QHBoxLayout(self._header)
        header_layout.setContentsMargins(8, 6, 8, 6)
        header_layout.setSpacing(8)
        header_layout.addWidget(self._toggle_button)
        header_layout.addWidget(self._title_label, stretch=1)

        self._content_container = QWidget()
        self._content_container.setObjectName("ExpandableSectionContent")

        self._content_layout = QVBoxLayout(self._content_container)
        self._content_layout.setContentsMargins(12, 8, 12, 12)
        self._content_layout.setSpacing(8)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self._header)
        main_layout.addWidget(self._content_container)

        if content is not None:
            self.set_content(content)

        self.set_expanded(initially_expanded)
        self.setStyleSheet(Stylesheets.load("common", "expandable_section.qss"))

    def set_content(self, widget: QWidget) -> None:
        self.clear_content()
        self._content_layout.addWidget(widget)

    def add_widget(self, widget: QWidget) -> None:
        self._content_layout.addWidget(widget)

    def clear_content(self) -> None:
        while self._content_layout.count():
            item = self._content_layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

    def is_expanded(self) -> bool:
        return self._expanded

    def toggle(self) -> None:
        self.set_expanded(not self._expanded)

    def set_expanded(self, expanded: bool) -> None:
        if self._expanded == expanded:
            self._apply_expanded_state()
            return

        self._expanded = expanded
        self._apply_expanded_state()
        self.toggled.emit(expanded)

    def _apply_expanded_state(self) -> None:
        self._content_container.setVisible(self._expanded)

        if self._expanded:
            self._toggle_button.setArrowType(Qt.ArrowType.DownArrow)
        else:
            self._toggle_button.setArrowType(Qt.ArrowType.RightArrow)

    def _on_header_pressed(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle()

        QWidget.mousePressEvent(self._header, event)