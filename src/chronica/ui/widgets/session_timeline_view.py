from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtQuick import QQuickView

from src.chronica.ui.presentation.models import (
    SessionTimeline,
)

from src.chronica.ui.presentation.bridges.session_timeline_bridge import SessionTimelineBridge
from src.chronica.common.timestamp import TimestampContext
import src.chronica.common.paths as paths

class SessionTimelineView(QQuickView):
    def __init__(self, ts_ctx: TimestampContext, parent=None) -> None:
        super().__init__(parent)

        self.timeline_bridge = SessionTimelineBridge(ts_ctx, self)
        self.rootContext().setContextProperty(
            "timelineBridge",
            self.timeline_bridge,
        )

        qml_path = (paths.UI_DIR / "qml" / "session_timeline" / "SessionTimelineView.qml").resolve()
        self.setSource(QUrl.fromLocalFile(str(qml_path)))
        self.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
    
    def set_timeline(self, timeline: SessionTimeline) -> None:
        self.timeline_bridge.set_timeline(timeline)