from __future__ import annotations
from src.chronica.common.resource_locator import ResourceLocator
from enum import StrEnum
import re

QSS_TOKEN_PATTERN = re.compile(r"\$([A-Za-z_][A-Za-z0-9_]*)\$")

class Stylesheets:
    @staticmethod
    def apply_variables(qss: str, variables: dict[str, str | int | float]) -> str:
        def replace(match: re.Match[str]) -> str:
            name = match.group(1)

            if name not in variables:
                raise KeyError(f"Unknown QSS variable: ${name}$")

            return str(variables[name])

        return QSS_TOKEN_PATTERN.sub(replace, qss)
    
    @staticmethod
    def load(*path_parts: str, **variables: str | int | float) -> str:
        qss = ResourceLocator.stylesheet(*path_parts).read_text(encoding="utf-8")
        
        if not variables:
            return qss
        
        return Stylesheets.apply_variables(qss, variables)

class QSS:
    class Property(StrEnum):
        FONT_STYLE = "font-style"
        FONT_WEIGHT = "font-weight"
        
    class Value:
        class FontStyle(StrEnum):
            ITALIC = "italic"
            
        class FontWeight(StrEnum):
            BOLD = "bold"

        class BorderStyle(StrEnum):
            SOLID = "solid"

        class Border(StrEnum):
            NONE = "none"
            
            @staticmethod
            def of(width: int, style: QSS.Value.BorderStyle, color: str) -> str:
                return f"{width}px {style.value} {color}"
    
    class PropertyLine:
        EMPTY = ""
        
        @staticmethod
        def maybe_decl(
            prop: QSS.Property,
            value: str | int | float | StrEnum | None
        ) -> str:
            return f"{prop.value}: {value.value if isinstance(value, StrEnum) else value};" \
                if value is not None else QSS.PropertyLine.EMPTY
        
        @staticmethod
        def font_style(style: QSS.Value.FontStyle | None) -> str:
            return QSS.PropertyLine.maybe_decl(QSS.Property.FONT_STYLE, style)
        
        @staticmethod
        def font_weight(weight: QSS.Value.FontWeight | int | None) -> str:
            return QSS.PropertyLine.maybe_decl(QSS.Property.FONT_WEIGHT, weight)