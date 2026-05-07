from __future__ import annotations

import hashlib
from datetime import datetime, timedelta

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QBrush, QPen, QPainter
from PySide6.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsSimpleTextItem,
    QGraphicsView,
)

from src.chronica.ui.presentation.models import (
    SessionTimeline,
    SessionTimelineRow,
    SessionTimelineSegment,
)


class _TimelineColorResolver:
    _PALETTE = [
        QColor("#4CC9F0"),
        QColor("#4895EF"),
        QColor("#4361EE"),
        QColor("#7209B7"),
        QColor("#F72585"),
        QColor("#06D6A0"),
        QColor("#FFBE0B"),
        QColor("#FB5607"),
    ]

    @classmethod
    def resolve(cls, color_key: str) -> QColor:
        digest = hashlib.blake2b(
            color_key.encode("utf-8"),
            digest_size=8,
        ).hexdigest()

        index = int(digest, 16) % len(cls._PALETTE)
        return QColor(cls._PALETTE[index])


def _floor_datetime_by_minutes(dt: datetime, minutes: int) -> datetime:
    floored_minute = (dt.minute // minutes) * minutes

    return dt.replace(
        minute=floored_minute,
        second=0,
        microsecond=0,
    )


def _ceil_datetime_by_minutes(dt: datetime, minutes: int) -> datetime:
    floored = _floor_datetime_by_minutes(dt, minutes)
    normalized = dt.replace(second=0, microsecond=0)

    if floored == normalized:
        return floored

    return floored + timedelta(minutes=minutes)


class SessionTimelineSegmentItem(QGraphicsRectItem):
    def __init__(
        self,
        segment: SessionTimelineSegment,
        row_index: int,
        rect: QRectF,
        base_color: QColor,
        owner: "SessionTimelineScene",
    ) -> None:
        super().__init__(rect)

        self.segment = segment
        self.row_index = row_index
        self.base_color = base_color
        self.owner = owner

        self.setAcceptHoverEvents(True)
        self.setZValue(10)

        self.setToolTip(self._make_tooltip())
        self.apply_normal_style()

    def _make_tooltip(self) -> str:
        if self.segment.tooltip:
            return self.segment.tooltip

        sd = self.segment.session

        return (
            f"{sd.app_name}\n"
            f"{sd.window_title}\n"
            f"{sd.start:%Y-%m-%d %H:%M:%S} → {sd.end:%Y-%m-%d %H:%M:%S}\n"
            f"{sd.duration}"
        )

    def apply_normal_style(self) -> None:
        color = QColor(self.base_color)
        color.setAlpha(145)

        self.setBrush(QBrush(color))
        self.setPen(QPen(Qt.PenStyle.NoPen))
        self.setZValue(10)

    def apply_row_highlight_style(self) -> None:
        color = QColor(self.base_color)
        color.setAlpha(225)

        self.setBrush(QBrush(color))
        self.setPen(QPen(QColor("#BFEFFF"), 1.1))
        self.setZValue(20)

    def apply_hover_style(self) -> None:
        color = QColor(self.base_color).lighter(135)
        color.setAlpha(255)

        self.setBrush(QBrush(color))
        self.setPen(QPen(QColor("#FFFFFF"), 2.0))
        self.setZValue(30)

    def hoverEnterEvent(self, event) -> None:
        self.owner.set_hovered_segment(
            segment_key=self.segment.key,
            row_index=self.row_index,
        )
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event) -> None:
        self.owner.clear_hovered_segment()
        super().hoverLeaveEvent(event)


class SessionTimelineScene(QGraphicsScene):
    def __init__(self) -> None:
        super().__init__()

        self.segment_items: list[SessionTimelineSegmentItem] = []
        self.hovered_segment_key: str | None = None
        self.hovered_row_index: int | None = None

    def add_segment_item(self, item: SessionTimelineSegmentItem) -> None:
        self.segment_items.append(item)
        self.addItem(item)

    def set_hovered_segment(self, segment_key: str, row_index: int) -> None:
        self.hovered_segment_key = segment_key
        self.hovered_row_index = row_index
        self.refresh_segment_styles()

    def clear_hovered_segment(self) -> None:
        self.hovered_segment_key = None
        self.hovered_row_index = None
        self.refresh_segment_styles()

    def refresh_segment_styles(self) -> None:
        for item in self.segment_items:
            if item.segment.key == self.hovered_segment_key:
                item.apply_hover_style()
            elif item.row_index == self.hovered_row_index:
                item.apply_row_highlight_style()
            else:
                item.apply_normal_style()


class SessionTimelineView(QGraphicsView):
    LABEL_WIDTH = 220
    TIMELINE_WIDTH = 900

    TOP_PADDING = 42
    BOTTOM_PADDING = 32

    ROW_HEIGHT = 42
    ROW_GAP = 8

    SEGMENT_HEIGHT = 20
    MIN_SEGMENT_WIDTH = 3.0

    TIME_RANGE_ROUNDING_MINUTES = 10
    TICK_INTERVAL_MINUTES = 10

    def __init__(self) -> None:
        super().__init__()

        self.timeline: SessionTimeline | None = None

        self.visible_start: datetime | None = None
        self.visible_end: datetime | None = None

        self.scene = SessionTimelineScene()
        self.setScene(self.scene)

        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setMouseTracking(True)
        self.setBackgroundBrush(QBrush(QColor("#111318")))
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

    def set_timeline(self, timeline: SessionTimeline) -> None:
        self.timeline = timeline
        self._resolve_visible_datetime_range()
        self._rebuild_scene()

    def _resolve_visible_datetime_range(self) -> None:
        if self.timeline is None:
            self.visible_start = None
            self.visible_end = None
            return

        all_segments = [
            segment
            for row in self.timeline.rows
            for segment in row.segments
        ]

        if not all_segments:
            self.visible_start = None
            self.visible_end = None
            return

        real_start = min(segment.session.start for segment in all_segments)
        real_end = max(segment.session.end for segment in all_segments)

        self.visible_start = _floor_datetime_by_minutes(
            real_start,
            self.TIME_RANGE_ROUNDING_MINUTES,
        )

        self.visible_end = _ceil_datetime_by_minutes(
            real_end,
            self.TIME_RANGE_ROUNDING_MINUTES,
        )

        if self.visible_start == self.visible_end:
            self.visible_end = self.visible_start + timedelta(
                minutes=self.TIME_RANGE_ROUNDING_MINUTES,
            )

    def _rebuild_scene(self) -> None:
        self.scene.clear()
        self.scene.segment_items.clear()
        self.scene.hovered_segment_key = None
        self.scene.hovered_row_index = None

        if self.timeline is None:
            return

        row_count = len(self.timeline.rows)

        scene_width = self.LABEL_WIDTH + self.TIMELINE_WIDTH + 80
        scene_height = (
            self.TOP_PADDING
            + row_count * (self.ROW_HEIGHT + self.ROW_GAP)
            + self.BOTTOM_PADDING
        )

        self.scene.setSceneRect(0, 0, scene_width, scene_height)

        self._draw_background(scene_width, scene_height)
        self._draw_time_axis()

        for row_index, row in enumerate(self.timeline.rows):
            self._draw_row(row_index, row)

    def _draw_background(self, width: float, height: float) -> None:
        self.scene.addRect(
            QRectF(0, 0, width, height),
            QPen(Qt.PenStyle.NoPen),
            QBrush(QColor("#111318")),
        )

        self.scene.addRect(
            QRectF(0, 0, self.LABEL_WIDTH, height),
            QPen(Qt.PenStyle.NoPen),
            QBrush(QColor("#171A21")),
        )

    def _draw_time_axis(self) -> None:
        if self.visible_start is None or self.visible_end is None:
            return

        axis_y = self.TOP_PADDING - 20

        self.scene.addLine(
            self.LABEL_WIDTH,
            axis_y,
            self.LABEL_WIDTH + self.TIMELINE_WIDTH,
            axis_y,
            QPen(QColor("#4A5160"), 1),
        )

        tick_dt = self.visible_start
        tick_delta = timedelta(minutes=self.TICK_INTERVAL_MINUTES)

        while tick_dt <= self.visible_end:
            x = self._datetime_to_x(tick_dt)

            self.scene.addLine(
                x,
                axis_y - 5,
                x,
                axis_y + 5,
                QPen(QColor("#6A7280"), 1),
            )

            label = QGraphicsSimpleTextItem(tick_dt.strftime("%H:%M"))
            label.setBrush(QBrush(QColor("#8F98A8")))
            label.setPos(x - 18, axis_y - 26)
            label.setZValue(40)

            self.scene.addItem(label)

            tick_dt += tick_delta

    def _draw_row(self, row_index: int, row: SessionTimelineRow) -> None:
        row_y = self._row_y(row_index)

        self._draw_row_label(row.label, row_y)
        self._draw_row_guide(row_y)

        for segment in row.segments:
            self._draw_segment(row_index, row_y, segment)

    def _draw_row_label(self, label: str, row_y: float) -> None:
        text = QGraphicsSimpleTextItem(label)
        text.setBrush(QBrush(QColor("#D7DEE9")))
        text.setPos(16, row_y + 10)
        text.setZValue(40)

        self.scene.addItem(text)

    def _draw_row_guide(self, row_y: float) -> None:
        line_y = row_y + self.ROW_HEIGHT / 2

        self.scene.addLine(
            self.LABEL_WIDTH,
            line_y,
            self.LABEL_WIDTH + self.TIMELINE_WIDTH,
            line_y,
            QPen(QColor("#2A2F3A"), 1),
        )

    def _draw_segment(
        self,
        row_index: int,
        row_y: float,
        segment: SessionTimelineSegment,
    ) -> None:
        rect = self._segment_rect(segment, row_y)
        color = _TimelineColorResolver.resolve(segment.color_key)

        item = SessionTimelineSegmentItem(
            segment=segment,
            row_index=row_index,
            rect=rect,
            base_color=color,
            owner=self.scene,
        )

        self.scene.add_segment_item(item)

    def _row_y(self, row_index: int) -> float:
        return self.TOP_PADDING + row_index * (self.ROW_HEIGHT + self.ROW_GAP)

    def _segment_rect(
        self,
        segment: SessionTimelineSegment,
        row_y: float,
    ) -> QRectF:
        start_x = self._datetime_to_x(segment.session.start)
        end_x = self._datetime_to_x(segment.session.end)

        width = max(self.MIN_SEGMENT_WIDTH, end_x - start_x)
        y = row_y + (self.ROW_HEIGHT - self.SEGMENT_HEIGHT) / 2

        return QRectF(
            start_x,
            y,
            width,
            self.SEGMENT_HEIGHT,
        )

    def _datetime_to_x(self, dt: datetime) -> float:
        if self.visible_start is None or self.visible_end is None:
            return self.LABEL_WIDTH

        total = self.visible_end - self.visible_start

        if total.total_seconds() <= 0:
            return self.LABEL_WIDTH

        offset = dt - self.visible_start
        ratio = offset / total

        return self.LABEL_WIDTH + ratio * self.TIMELINE_WIDTH