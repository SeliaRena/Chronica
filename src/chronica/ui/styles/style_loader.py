from pathlib import Path
from src.chronica.common.paths import STYLES_DIR

def load_stylesheet(sheetname: str) -> str:
    sheet_path = STYLES_DIR / f"{sheetname}.qss"
    return sheet_path.read_text(encoding="utf-8")