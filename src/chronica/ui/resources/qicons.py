from __future__ import annotations

from PySide6.QtGui import QIcon
from PySide6.QtCore import QFileInfo, Qt
from PySide6.QtWidgets import QFileIconProvider, QLabel

from src.chronica.common.resource_locator import ResourceLocator

from pathlib import Path

_GLOBAL_ICON_CACHE: dict[str, QIcon] = {}

class QIcons:
    @staticmethod
    def load(*path_parts: str) -> QIcon:
        return QIcon(str(ResourceLocator.ui_icon(*path_parts)))
    
    @staticmethod
    def preload_ui_icons() -> None:
        for icon_path in ResourceLocator.ui_icon().iterdir():
            filename = icon_path.name
            _GLOBAL_ICON_CACHE[filename] = QIcon(str(icon_path))

    @staticmethod
    def get(filename: str) -> QIcon:
        if filename not in _GLOBAL_ICON_CACHE:
            raise ValueError(f"Unregistered icon: {filename}")
        
        return _GLOBAL_ICON_CACHE[filename]
    
    @staticmethod
    def make_icon_label(icon: QIcon, *, w: int = 24, h: int = 24, object_name: str | None = None) -> QLabel:
        """
        Simple function to create a QLabel with the given icon. \n
        This is useful when you need to make an atomic widget out of an icon, and have free control over its
        objectName to set whatever stylesheet you want. \n\n
        
        initialized properties: \n
        - scaledContents (True) \n
        - fixedSize (w, h) \n
        - alignment (center) \n
        - pixmap (icon.pixmap(w, h)) \n
        - objectName (optional objectName, will not set if arg is None) \n
        """
        
        label = QLabel()
        label.setScaledContents(True)
        label.setFixedSize(w, h)
        label.setPixmap(icon.pixmap(w, h))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        if object_name is not None:
            label.setObjectName(object_name)
        
        return label

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
        return QIcons.get("software.png")