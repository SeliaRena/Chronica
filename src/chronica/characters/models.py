from dataclasses import dataclass
from collections.abc import Mapping, Iterable
from typing import Any

@dataclass(frozen=True, slots=True)
class RenderedLine:
    key: str
    text: str
    expression: str | None

@dataclass(frozen=True, slots=True)
class Line:
    key: str
    text: str
    expression: str | None = None

    def render(self, context: Mapping[str, Any] | None = None) -> RenderedLine:
        return RenderedLine(
            key=self.key,
            text=self.text.format(**(context or {})),
            expression=self.expression
        )

type LineKey = str
type DialogueKey = str
type LineRenderContext = Mapping[str, Any]
type DialogueRenderContext = Mapping[LineKey, LineRenderContext]

@dataclass(frozen=True, slots=True)
class RenderedDialogue:
    key: str
    lines: tuple[RenderedLine, ...]

class DialogueTemplate:
    def __init__(self, key: str, lines: Iterable[Line]):
        self.key: str = key
        self._lines: dict[LineKey, Line] = {line.key: line for line in lines}

    def __len__(self):
        return len(self._lines)

    def __iter__(self):
        return iter(self._lines.values())

    def __getitem__(self, key: LineKey) -> Line | None:
        return self._lines.get(key)

    def render(self, context: DialogueRenderContext | None = None) -> RenderedDialogue:
        context = context or {}
        
        return RenderedDialogue(
            key=self.key,
            lines=tuple(
                line.render(context.get(line.key, None))
                for line in self._lines.values()
            ),
        )