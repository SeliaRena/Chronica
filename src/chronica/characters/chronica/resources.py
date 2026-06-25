from src.chronica.common.resource_locator import ResourceLocator
from pathlib import Path

from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

EXPRESSIONS_DIR = ResourceLocator.character_asset("chronica", "expressions")
type ExpressionKey = str

class Expressions:
    EXPRESSIONS_STORE: dict[ExpressionKey, QPixmap] = {}
    
    @classmethod
    def preload_expressions(cls):
        for expression in EXPRESSIONS_DIR.iterdir():
            if expression.is_file() and expression.suffix in [".png", ".jpg", ".jpeg"]:
                key = expression.stem
                pixmap = QPixmap(str(expression))
                cls.EXPRESSIONS_STORE[key] = pixmap

    @classmethod
    def get(cls, key: ExpressionKey) -> QPixmap:
        if key not in cls.EXPRESSIONS_STORE:
            raise KeyError(f"Expression '{key}' not found in store.")
        return cls.EXPRESSIONS_STORE[key]