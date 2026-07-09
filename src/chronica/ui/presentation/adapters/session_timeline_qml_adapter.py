from __future__ import annotations

from typing import Any, Literal
from datetime import datetime
import hashlib

from src.chronica.ui.presentation.models.session_timeline_models import (
    SessionTimeline,
    SessionTimelineRow,
    SessionTimelineSegment,
)

from src.chronica.ui.presentation.formatters import (
    ymd_hms,
    hms,
    simplistic_simplified_ms,
)

from src.chronica.common.timestamp import TimestampContext
import src.chronica.ui.presentation.models.session_timeline_models as session_timeline

ONE_SECOND_MS = 1000.0
FIVE_MINUTES_MS = 5 * 60 * ONE_SECOND_MS
TINY_SEGMENT_WIDTH = 10
MIN_SEGMENT_WIDTH = 5

class SessionTimelineQmlAdapter:
    def __init__(self, ts_ctx: TimestampContext) -> None:
        self._ts_ctx = ts_ctx
        self._timeline: SessionTimeline | None = None
        self._visible_start_ts_ms: int = 0
        self._visible_end_ts_ms: int = 0

    def to_model(self, timeline: SessionTimeline) -> dict[str, Any]:
        self._timeline = timeline
        self._visible_start_ts_ms, self._visible_end_ts_ms = self._visible_range_ms(timeline)
        
        return session_timeline.QmlData(
            visible_start_ts_ms=self._visible_start_ts_ms,
            visible_end_ts_ms=self._visible_end_ts_ms,
            axis_ticks=self._create_qml_axis_ticks(),
            rows=tuple(self._to_qml_row(r) for r in self._timeline.rows),
        ).to_view_dict()

    def _create_qml_axis_ticks(self) -> tuple[session_timeline.QmlAxisTick, ...]:
        if self._timeline is None:
            return ()
        
        ticks: list[session_timeline.QmlAxisTick] = []
        current_tick_ms = self._visible_start_ts_ms
        
        while current_tick_ms <= self._visible_end_ts_ms:
            tick_dt: datetime = self._ts_ctx.datetime_from_ts_ms(current_tick_ms)
            tick_kind: Literal["day_boundary", "minor"] = "day_boundary" if tick_dt.hour == 0 and tick_dt.minute == 0 else "minor"
            tick_label: str = ymd_hms(tick_dt) if tick_kind == "day_boundary" else hms(tick_dt)
            
            ticks.append(
                session_timeline.QmlAxisTick(
                    real_x=(current_tick_ms - self._visible_start_ts_ms) / ONE_SECOND_MS,
                    timestamp_ms=current_tick_ms,
                    label=tick_label,
                    kind=tick_kind,
                )
            )
            
            current_tick_ms += FIVE_MINUTES_MS
        
        return tuple(ticks)
    
    def _to_qml_row(self, row: SessionTimelineRow) -> session_timeline.QmlRow:
        repeater_items: list[session_timeline.QmlRepeaterItem] = []
        tiny_buffer: list[session_timeline.QmlSegment] = []
        real_width_accum: float = 0.0
        last_end_ts_ms: int = -1
        
        for s in row.segments:
            qml_s = self._to_qml_segment(s)
            
            if not qml_s.tiny:
                clustered_item = self._try_create_clustered_repeater_item(tiny_buffer, real_width_accum)
                if clustered_item is not None:
                    repeater_items.append(clustered_item)
                    tiny_buffer.clear()
                    real_width_accum = 0.0
                
                repeater_items.append(
                    session_timeline.QmlRepeaterItem(
                        kind="normal",
                        draw_x=qml_s.real_x,
                        draw_width=qml_s.real_width,
                        hit_test_width=qml_s.real_width,
                        segments=(qml_s,),
                        tooltip=qml_s.tooltip,
                    )
                )
            else:
                if last_end_ts_ms != -1 and self._to_epoch_ms(s.session.start) > last_end_ts_ms:
                    clustered_item = self._try_create_clustered_repeater_item(tiny_buffer, real_width_accum)
                    if clustered_item is not None:
                        repeater_items.append(clustered_item)
                        tiny_buffer.clear()
                        real_width_accum = 0.0
                
                tiny_buffer.append(qml_s)
                real_width_accum += qml_s.real_width
            
            last_end_ts_ms = self._to_epoch_ms(s.session.end)
        
        clustered_item = self._try_create_clustered_repeater_item(tiny_buffer, real_width_accum)
        if clustered_item is not None:
            repeater_items.append(clustered_item)
        
        return session_timeline.QmlRow(
            label=row.label,
            repeater_items=tuple(repeater_items),
        )

    def _try_create_clustered_repeater_item(
        self, 
        tiny_buffer: list[session_timeline.QmlSegment], 
        real_width_accum: float
    ) -> session_timeline.QmlRepeaterItem | None:
        if tiny_buffer:
            return session_timeline.QmlRepeaterItem(
                kind="clustered",
                draw_x=tiny_buffer[0].real_x,
                draw_width=max(MIN_SEGMENT_WIDTH, real_width_accum),
                hit_test_width=max(MIN_SEGMENT_WIDTH, real_width_accum),
                segments=tuple(tiny_buffer),
                tooltip=f"This is a Clustered Segment\n\n"
                f"From {tiny_buffer[0].session.start_dt_text} to {tiny_buffer[-1].session.end_dt_text}\n"
                f"Duration: {simplistic_simplified_ms(sum(tiny_s.session.duration_ms for tiny_s in tiny_buffer))}\n"
                f"Contains {len(tiny_buffer)} activities.",
            )
        return None

    def _to_qml_segment(self, segment: SessionTimelineSegment) -> session_timeline.QmlSegment:
        return session_timeline.QmlSegment(
            real_x=self._get_segment_start_x(segment),
            real_width=self._get_segment_width(segment),
            color=self._resolve_color(segment.color_key),
            session=session_timeline.QmlSession(
                app_name=segment.session.app_name,
                app_path=segment.session.app_path,
                window_title=segment.session.window_title,
                start_ts_ms=self._to_epoch_ms(segment.session.start),
                end_ts_ms=self._to_epoch_ms(segment.session.end),
                start_dt_text=ymd_hms(segment.session.start),
                end_dt_text=ymd_hms(segment.session.end),
                duration_ms=segment.session.duration.total_ms,
                duration_text=simplistic_simplified_ms(segment.session.duration),
                timezone_info=segment.session.start.tzname() if segment.session.start.tzinfo else "Unknown",
            ),
            tiny=self._get_segment_width(segment) < TINY_SEGMENT_WIDTH,
            tooltip=f"{segment.session.app_name} - {segment.session.window_title}\n"
            f"From {ymd_hms(segment.session.start)} to {ymd_hms(segment.session.end)}\n"
            f"Duration: {simplistic_simplified_ms(segment.session.duration)}\n\n"
            f"App Path: {segment.session.app_path}",
        )

    def _get_segment_start_x(self, segment: SessionTimelineSegment) -> float:
        segment_start_ts_ms = self._to_epoch_ms(segment.session.start)
        delta = segment_start_ts_ms - self._visible_start_ts_ms
        return delta / ONE_SECOND_MS # 1 second = 1 pixel in the QML timeline view
    
    def _get_segment_width(self, segment: SessionTimelineSegment) -> float:
        segment_start_ts_ms = self._to_epoch_ms(segment.session.start)
        segment_end_ts_ms = self._to_epoch_ms(segment.session.end)
        delta = segment_end_ts_ms - segment_start_ts_ms
        return delta / ONE_SECOND_MS # 1 second = 1 pixel in the QML timeline view

    @classmethod
    def _visible_range_ms(cls, timeline: SessionTimeline) -> tuple[int, int]:
        starts: list[int] = []
        ends: list[int] = []

        for row in timeline.rows:
            for segment in row.segments:
                starts.append(cls._to_epoch_ms(segment.session.start))
                ends.append(cls._to_epoch_ms(segment.session.end))

        if not starts or not ends:
            return 0, 0

        raw_start = min(starts)
        raw_end = max(ends)
        
        visible_start = raw_start - (raw_start % FIVE_MINUTES_MS)
        visible_end = raw_end + (FIVE_MINUTES_MS - (raw_end % FIVE_MINUTES_MS)) if raw_end % FIVE_MINUTES_MS != 0 else raw_end

        return visible_start, visible_end

    @staticmethod
    def _to_epoch_ms(dt: datetime) -> int:
        return int(dt.timestamp() * 1000)

    @staticmethod
    def _resolve_color(color_key: str) -> str:
        palette = [
            "#22d3ee",
            "#38bdf8",
            "#3b82f6",
            "#6366f1",
            "#8b5cf6",
            "#c026d3",
            "#db2777",
            "#fbbf24",
        ]
        
        digest = hashlib.sha256(color_key.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % len(palette)
        
        return palette[index]