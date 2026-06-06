from __future__ import annotations

from src.chronica.characters.models import (
    LineKey,
    LineRenderContext,
    DialogueRenderContext
)

class DialogueRenderContextBuilder:
    def __init__(self) -> None:
        self._context: dict[LineKey, LineRenderContext] = {}

    def with_line_render_context(self, line_key: LineKey, **kwargs) -> DialogueRenderContextBuilder:
        self._context[line_key] = kwargs
        return self

    def build(self) -> DialogueRenderContext:
        return self._context