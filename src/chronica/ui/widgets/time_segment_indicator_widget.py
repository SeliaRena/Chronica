from __future__ import annotations

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QPolygonF
from PySide6.QtWidgets import QWidget

class TimeSegmentIndicatorWidget(QWidget):
    """
    Draws a visual indicator for one time segment:

        ●
        │
        │──────▶
        │
        ●

    Intended to be used inside a row layout:

        HBox[
            TimeLabelColumn,
            TimeSegmentIndicatorWidget,
            ChipWidget
        ]
    """

    def __init__(
        self,
        *,
        show_top_node: bool = True,
        show_bottom_node: bool = True,
        show_vertical_line: bool = True,
        show_arrow: bool = True,
        highlighted: bool = False,
        node_radius: int = 4,
        line_width: int = 2,
        arrow_head_size: int = 8,
        timeline_x: int = 12,
        top_padding: int = 8,
        bottom_padding: int = 8,
        min_width: int = 72,
        fixed_height: int | None = 72,
        line_color: QColor | str = "#4B5563",
        node_color: QColor | str = "#D1D5DB",
        arrow_color: QColor | str = "#9CA3AF",
        highlight_color: QColor | str = "#E5E7EB",
        parent=None,
    ):
        super().__init__(parent)

        self.show_top_node = show_top_node
        self.show_bottom_node = show_bottom_node
        self.show_vertical_line = show_vertical_line
        self.show_arrow = show_arrow
        self.highlighted = highlighted

        self.node_radius = node_radius
        self.line_width = line_width
        self.arrow_head_size = arrow_head_size
        self.timeline_x = timeline_x
        self.top_padding = top_padding
        self.bottom_padding = bottom_padding

        self.line_color = QColor(line_color)
        self.node_color = QColor(node_color)
        self.arrow_color = QColor(arrow_color)
        self.highlight_color = QColor(highlight_color)

        self.setMinimumWidth(min_width)

        if fixed_height is not None:
            self.setFixedHeight(fixed_height)
        else:
            self.setMinimumHeight(48)

    def set_highlighted(self, highlighted: bool) -> None:
        if self.highlighted == highlighted:
            return

        self.highlighted = highlighted
        self.update()

    def set_top_node_visible(self, visible: bool) -> None:
        if self.show_top_node == visible:
            return

        self.show_top_node = visible
        self.update()

    def set_bottom_node_visible(self, visible: bool) -> None:
        if self.show_bottom_node == visible:
            return

        self.show_bottom_node = visible
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()

        x = float(self.timeline_x)
        top_y = float(self.top_padding)
        bottom_y = float(height - self.bottom_padding)
        mid_y = height / 2.0

        active_line_color = self.highlight_color if self.highlighted else self.line_color
        active_arrow_color = self.highlight_color if self.highlighted else self.arrow_color
        active_node_color = self.highlight_color if self.highlighted else self.node_color

        if self.show_vertical_line:
            pen = QPen(active_line_color, self.line_width)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawLine(QPointF(x, top_y), QPointF(x, bottom_y))

        if self.show_arrow:
            self._draw_arrow(
                painter=painter,
                start=QPointF(x + self.line_width, mid_y),
                end=QPointF(width - self.arrow_head_size - 4, mid_y),
                color=active_arrow_color,
            )

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(active_node_color))

        if self.show_top_node:
            painter.drawEllipse(QPointF(x, top_y), self.node_radius, self.node_radius)

        if self.show_bottom_node:
            painter.drawEllipse(QPointF(x, bottom_y), self.node_radius, self.node_radius)

    def _draw_arrow(
        self,
        *,
        painter: QPainter,
        start: QPointF,
        end: QPointF,
        color: QColor,
    ) -> None:
        head_size = self.arrow_head_size

        # 防止 widget 太窄時箭頭反向或畫爆
        if end.x() <= start.x() + head_size:
            return

        pen = QPen(color, self.line_width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        painter.setPen(pen)
        painter.setBrush(QBrush(color))

        line_end = QPointF(end.x() - head_size, end.y())
        painter.drawLine(start, line_end)

        arrow_head = QPolygonF(
            [
                QPointF(end.x(), end.y()),
                QPointF(end.x() - head_size, end.y() - head_size / 2),
                QPointF(end.x() - head_size, end.y() + head_size / 2),
            ]
        )

        painter.drawPolygon(arrow_head)