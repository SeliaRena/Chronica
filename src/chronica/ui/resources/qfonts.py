from __future__ import annotations

from PySide6.QtGui import (
    QFontDatabase,
    QFont
)

from src.chronica.common.resource_locator import ResourceLocator

from pathlib import Path

class QFonts:
    @staticmethod
    def register(font_path: Path) -> None:
        font_id = QFontDatabase.addApplicationFont(str(font_path))
        
        if font_id == -1:
            raise RuntimeError(f"Failed to load font: {font_path}")

        families = QFontDatabase.applicationFontFamilies(font_id)

        if not families:
            raise RuntimeError(f"No font family found in: {font_path}")
    
    @staticmethod
    def load_directory(dir_path: Path) -> None:
        for font_path in dir_path.iterdir():
            QFonts.register(font_path)
    
    @staticmethod
    def load_all_ui_fonts() -> None:
        QFonts.load_directory(ResourceLocator.ui_font())