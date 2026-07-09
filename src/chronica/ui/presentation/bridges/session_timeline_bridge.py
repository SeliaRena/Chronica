from __future__ import annotations

from typing import Any

from PySide6.QtCore import QObject, Property, Signal

from src.chronica.ui.presentation.adapters.session_timeline_qml_adapter import (
    SessionTimelineQmlAdapter,
)
from src.chronica.ui.presentation.models import SessionTimeline
from src.chronica.common.timestamp import TimestampContext

class SessionTimelineBridge(QObject):
    modelChanged = Signal()

    def __init__(self, ts_ctx: TimestampContext, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._ts_ctx = ts_ctx
        self._qml_adapter = SessionTimelineQmlAdapter(ts_ctx)
        self._model: dict[str, Any] = {}

    @Property("QVariantMap", notify=modelChanged)
    def model(self) -> dict[str, Any]:
        return self._model

    def set_timeline(self, timeline: SessionTimeline) -> None:
        self._model = self._qml_adapter.to_model(timeline)
        self.modelChanged.emit()