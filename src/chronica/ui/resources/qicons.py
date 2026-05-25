from PySide6.QtGui import QIcon
from PySide6.QtCore import QFileInfo
from PySide6.QtWidgets import QFileIconProvider

from src.chronica.common.resource_locator import ResourceLocator

from pathlib import Path

class QIcons:
    @staticmethod
    def load(*path_parts: str) -> QIcon:
        return QIcon(str(ResourceLocator.ui_icon(*path_parts)))

class AppIconProvider:
    def __init__(self):
        self._provider = QFileIconProvider()
        self._cache: dict[str, QIcon] = {}

    def icon_for_path(self, app_path: str | Path | None) -> QIcon:
        if app_path is None:
            return self.fallback_icon()

        path = Path(app_path)

        if not path.exists():
            return self.fallback_icon()

        cache_key = str(path.resolve())

        if cache_key in self._cache:
            return self._cache[cache_key]

        icon = self._provider.icon(QFileInfo(str(path)))

        if icon.isNull():
            icon = self.fallback_icon()

        self._cache[cache_key] = icon
        return icon

    def fallback_icon(self) -> QIcon:
        return QIcons.load("application.svg")