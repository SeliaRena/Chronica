from PySide6.QtGui import QFontDatabase, QFont
from pathlib import Path

def load_font(font_path: Path, point_size: int = 12) -> QFont:
    font_id = QFontDatabase.addApplicationFont(str(font_path))

    if font_id == -1:
        raise RuntimeError(f"Failed to load font: {font_path}")

    families = QFontDatabase.applicationFontFamilies(font_id)

    if not families:
        raise RuntimeError(f"No font family found in: {font_path}")

    return QFont(families[0], point_size)