from __future__ import annotations
from enum import Enum, auto
from dataclasses import dataclass
from collections.abc import Callable
import re
from typing import ClassVar

ONE_MILLISECOND = 1
ONE_SECOND = 1000 * ONE_MILLISECOND
ONE_MINUTE = 60 * ONE_SECOND
ONE_HOUR = 60 * ONE_MINUTE
ONE_DAY = 24 * ONE_HOUR
ONE_WEEK = 7 * ONE_DAY

@dataclass(frozen=True)
class ChronoScaleMeta:
    name: str
    label: str
    ms_factor: int
    rank: int

class ChronoScale(Enum):
    MILLISECOND = ChronoScaleMeta("millisecond", "ms", ONE_MILLISECOND, 0)
    SECOND = ChronoScaleMeta("second", "sec", ONE_SECOND, 1)
    MINUTE = ChronoScaleMeta("minute", "min", ONE_MINUTE, 2)
    HOUR = ChronoScaleMeta("hour", "hr", ONE_HOUR, 3)
    DAY = ChronoScaleMeta("day", "day", ONE_DAY, 4)
    WEEK = ChronoScaleMeta("week", "wk", ONE_WEEK, 5)
    
    @property
    def scale_name(self) -> str:
        return self.value.name
    
    @property
    def label(self) -> str:
        return self.value.label
    
    @property
    def ms_factor(self) -> int:
        return self.value.ms_factor
    
    @property
    def rank(self) -> int:
        return self.value.rank

_RANK_TO_SCALE = tuple(sorted((scale for scale in ChronoScale), key=lambda s: s.rank))

@dataclass(frozen=True, slots=True)
class ChronoScaleInterval:
    lower_bound: ChronoScale
    upper_bound: ChronoScale
    
    def __post_init__(self):
        if self.lower_bound.rank > self.upper_bound.rank:
            raise ValueError(f"Invalid ChronoScaleInterval: lower_bound {self.lower_bound} has higher rank than upper_bound {self.upper_bound}")
    
    def __contains__(self, scale: ChronoScale) -> bool:
        return self.lower_bound.rank <= scale.rank <= self.upper_bound.rank

@dataclass(frozen=True, slots=True)
class ChronoSpan:
    value: int
    scale: ChronoScale
    
    @property
    def ms_factor(self) -> int:
        return self.scale.ms_factor
    
    @property
    def in_ms(self) -> int:
        return self.value * self.ms_factor
    
    def __str__(self) -> str:
        return f"{self.value}{self.scale.label}"
    
    def as_scale(self, target_scale: ChronoScale) -> tuple[ChronoSpan, ChronoSpan]:
        total_ms = self.in_ms
        target_value = total_ms // target_scale.ms_factor
        remainder_ms = total_ms % target_scale.ms_factor
        return ChronoSpan(target_value, target_scale), ChronoSpan(remainder_ms, ChronoScale.MILLISECOND)
    
    def __rshift__(self, target_scale: ChronoScale) -> tuple[ChronoSpan, ChronoSpan]:
        return self.as_scale(target_scale)
    
    def as_ratio(self, target_scale: ChronoScale) -> float:
        return self.in_ms / target_scale.ms_factor

# ===== Helpers =====
    
def upscale(current_scale: ChronoScale) -> ChronoScale | None:
    current_rank = current_scale.rank
    if current_rank < len(_RANK_TO_SCALE) - 1:
        return _RANK_TO_SCALE[current_rank + 1]
    return None

def downscale(current_scale: ChronoScale) -> ChronoScale | None:
    current_rank = current_scale.rank
    if current_rank > 0:
        return _RANK_TO_SCALE[current_rank - 1]
    return None

# ===== End of Helpers =====

class CascadingType(Enum):
    MINIMAL = auto()
    INTERVAL_LIKE = auto()
    FULL_PADDED = auto()

@dataclass(frozen=True, slots=True)
class CascadedChronoSpan:
    # Precompute zero spans for all scales to optimize the padding methods.
    # all_zeroes is rank based ordered, not cascaded span ordered.
    # You will need to REVERSE it when instantiating a cascaded span with it.
    _ALL_ZEROES: ClassVar[tuple[ChronoSpan, ...]] = tuple(ChronoSpan(0, scale) for scale in ChronoScale)
    
    total_ms: int
    inner_ordered_spans: tuple[ChronoSpan, ...]
    cascading_type: CascadingType = CascadingType.MINIMAL
    
    def __post_init__(self):
        normalized = self._normalize(self.inner_ordered_spans)
        object.__setattr__(self, "inner_ordered_spans", normalized)
        
    @staticmethod
    def _is_ordered(x: tuple[ChronoSpan, ...]) -> bool:
        return all(x[i].scale.rank > x[i + 1].scale.rank for i in range(len(x) - 1))
    
    @staticmethod
    def _dup_exists(x: tuple[ChronoSpan, ...]) -> bool:
        return len({span.scale for span in x}) != len(x)
    
    @staticmethod
    def _reorder(x: tuple[ChronoSpan, ...]) -> tuple[ChronoSpan, ...]:
        return tuple(sorted(x, key=lambda span: span.scale.rank, reverse=True))
    
    @classmethod
    def _normalize(cls, x: tuple[ChronoSpan, ...]) -> tuple[ChronoSpan, ...]:
        if cls._dup_exists(x):
            raise ValueError("Duplicate scales found in spans: " + ", ".join(span.scale.name for span in x))
        if not cls._is_ordered(x):
            return cls._reorder(x)
        return x
        
    @staticmethod
    def _all_0s() -> list[ChronoSpan]:
        return list(CascadedChronoSpan._ALL_ZEROES)
        
    @staticmethod
    def _cascade(total_ms: int) -> tuple[ChronoSpan, ...]:
        spans: list[ChronoSpan] = []
        remainder_span = ChronoSpan(total_ms, ChronoScale.MILLISECOND)
        target_scale = ChronoScale.WEEK
        
        while remainder_span.value > 0 and target_scale is not None:
            quotient_span, remainder_span = remainder_span >> target_scale
            if quotient_span.value > 0:
                spans.append(quotient_span)
            target_scale = downscale(target_scale)
        
        return tuple(spans)
    
    @property
    def max_span(self) -> ChronoSpan | None:
        for span in self.inner_ordered_spans:
            if span.value > 0:
                return span
        return None
    
    @property
    def min_span(self) -> ChronoSpan | None:
        for span in reversed(self.inner_ordered_spans):
            if span.value > 0:
                return span
        return None
    
    @classmethod
    def from_total_ms(cls, total_ms: int) -> CascadedChronoSpan:
        return cls(total_ms, cls._cascade(total_ms))
    
    @classmethod
    def from_span(cls, span: ChronoSpan) -> CascadedChronoSpan:
        return cls(span.in_ms, cls._cascade(span.in_ms))
    
    @classmethod
    def zero(cls, cascading_type: CascadingType = CascadingType.MINIMAL) -> CascadedChronoSpan:
        if cascading_type == CascadingType.FULL_PADDED:
            return cls(0, tuple(reversed(cls._all_0s())), cascading_type)
        return cls(0, tuple(), cascading_type)
    
    def _fill0buffer_and_justify(self) -> tuple[ChronoSpan, ...]:
        buf = type(self)._all_0s()
        for span in self.inner_ordered_spans:
            index = span.scale.rank
            buf[index] = span
        return tuple(reversed(buf))
    
    def _full_padded(self) -> CascadedChronoSpan:
        return CascadedChronoSpan(self.total_ms, self._fill0buffer_and_justify(), CascadingType.FULL_PADDED)
    
    def _minimized(self) -> CascadedChronoSpan:
        return type(self).from_total_ms(self.total_ms)
    
    def _interval_like(self) -> CascadedChronoSpan:
        l = self.min_span
        r = self.max_span
        if l is None or r is None:
            return type(self).zero(CascadingType.INTERVAL_LIKE)
        ret = tuple(span for span in self._fill0buffer_and_justify() if span.scale in ChronoScaleInterval(l.scale, r.scale))
        return CascadedChronoSpan(self.total_ms, ret, CascadingType.INTERVAL_LIKE)
    
    def transform(self, target_type: CascadingType) -> CascadedChronoSpan:
        if self.cascading_type == target_type:
            return self
        elif target_type == CascadingType.FULL_PADDED:
            return self._full_padded()
        elif target_type == CascadingType.MINIMAL:
            return self._minimized()
        elif target_type == CascadingType.INTERVAL_LIKE:
            return self._interval_like()
        else:
            raise ValueError(f"Unknown target cascading type: {target_type}")
    
    def __str__(self):
        return " ".join(str(span) for span in self.inner_ordered_spans)
    
# =======================================
# Formatting utilities
# =======================================

# ===== Lexical Analysis for ChronoPattern =====

_SIGIL = '$'
_KEYWORD_PART_PATTERN = r"\[(?P<keyword>[a-zA-Z0-9_]+)\]"
_FUNCTION_PART_PATTERN = r"\.(?P<function>[a-zA-Z_]+)\((?P<args>[^)]*)\)"
_RAW_CHRONO_TOKEN_REGEX = re.compile(fr"{re.escape(_SIGIL)}{_KEYWORD_PART_PATTERN}(?:{_FUNCTION_PART_PATTERN})?")

@dataclass(frozen=True)
class _LiteralToken:
    value: str

@dataclass(frozen=True)
class _KeywordToken:
    start: int
    end: int
    raw: str
    keyword: str
    function: str | None = None
    args: tuple[str, ...] | None = None
    
    @classmethod
    def from_match(cls, match: re.Match) -> _KeywordToken:
        raw = match.group(0)
        keyword = match.group("keyword")
        function = match.group("function")
        args_str = match.group("args")
        
        if function is None:
            return cls(match.start(), match.end(), raw, keyword, None, None)
        elif args_str == "":
            return cls(match.start(), match.end(), raw, keyword, function, ())
        else:
            args = tuple(arg.strip() for arg in args_str.split(","))
            if any(arg == "" for arg in args):
                raise ValueError(f"Invalid empty argument in function call: {raw!r}")
            return cls(match.start(), match.end(), raw, keyword, function, args)
        
type _ChronoToken = _LiteralToken | _KeywordToken
type _TokenizedResult = tuple[_ChronoToken, ...]

# ===== Parsing utilities for ChronoPattern =====

type ChronoSpanExtractor = Callable[[ChronoSpan], str]
_KEYWORD_OPS_REGISTRY: dict[str, ChronoSpanExtractor] = {
    "value": lambda span: str(span.value),
    "scalename": lambda span: span.scale.scale_name,
    "scalelabel": lambda span: span.scale.label
}

def _pad(target: str, width: int, pad_char: str = '0') -> str:
    return target.rjust(width, pad_char)

def _pad_adapter(target: str, args: tuple[str, ...]) -> str:
    if not (0 < len(args) <= 2):
        raise ValueError(f"Post-processing function 'pad()' expects 1 or 2 arguments, got {len(args)}")
    try:
        width = int(args[0])
    except ValueError as e:
        raise ValueError(f"Invalid width argument for padding function: {args[0]!r}") from e

    pad_char = args[1] if len(args) == 2 else '0'
    if len(pad_char) != 1:
        raise ValueError(f"Pad character must be a single character: {pad_char!r}")
    
    return _pad(target, width, pad_char)

type PostProcessorAdapter = Callable[[str, tuple[str, ...]], str]
_POST_PROCESSORS_REGISTRY: dict[str, PostProcessorAdapter] = {
    "pad": _pad_adapter
}

# ===== ChronoSpanFormatter and CascadedChronoSpanFormatter =====

class ChronoSpanFormatter:
    def __init__(self, keyword_ops: dict[str, ChronoSpanExtractor] | None = None,
                 post_processors: dict[str, PostProcessorAdapter] | None = None):
        self.keyword_ops = keyword_ops or _KEYWORD_OPS_REGISTRY
        self.post_processors = post_processors or _POST_PROCESSORS_REGISTRY
        self.is_compiled: bool = False
        self._tokenized_cache: _TokenizedResult | None = None
        
    def _tokenize(self, pattern: str) -> _TokenizedResult:
        keyword_tokens = tuple(_KeywordToken.from_match(match) for match in _RAW_CHRONO_TOKEN_REGEX.finditer(pattern))
        tokens = []
        last_index = 0
        
        for keyword_token in keyword_tokens:
            if keyword_token.start > last_index:
                literal_value = pattern[last_index:keyword_token.start]
                tokens.append(_LiteralToken(literal_value))
            tokens.append(keyword_token)
            last_index = keyword_token.end
        
        if last_index < len(pattern):
            literal_value = pattern[last_index:]
            tokens.append(_LiteralToken(literal_value))
        
        return tuple(tokens)
    
    def _validate(self, tokenized: _TokenizedResult):
        for token in tokenized:
            if isinstance(token, _KeywordToken):
                if token.keyword not in self.keyword_ops:
                    raise ValueError(f"Unknown keyword in pattern: {token.keyword!r}")
                if token.function is not None and token.function not in self.post_processors:
                    raise ValueError(f"Unknown post-processing function in pattern: {token.function!r}")
            
    def _resolve_pattern_with(self, span: ChronoSpan) -> tuple[str, ...]:
        values = []
        for token in self._tokenized_cache:
            resolved_token_str = ""
            
            if isinstance(token, _LiteralToken):
                resolved_token_str = token.value
            elif isinstance(token, _KeywordToken):
                extractor = self.keyword_ops[token.keyword]
                resolved_token_str = extractor(span)
                if token.function is not None:
                    post_processor = self.post_processors[token.function]
                    resolved_token_str = post_processor(resolved_token_str, token.args)
                    
            values.append(resolved_token_str)
        return tuple(values)

    def compile(self, pattern: str):
        tokenized = self._tokenize(pattern)
        
        try:
            self._validate(tokenized)
        except ValueError as e:
            raise ValueError(f"Invalid pattern: {pattern!r}") from e
        
        self._tokenized_cache = tokenized
        self.is_compiled = True
        return self
    
    def format(self, span: ChronoSpan) -> str:
        if not self.is_compiled:
            raise RuntimeError("Formatter must be compiled with a pattern before formatting.")
        
        formatted = "".join(self._resolve_pattern_with(span))
        return formatted
    
    def __getitem__(self, span: ChronoSpan) -> str:
        return self.format(span)

# TODO: Separate formatter with formatter builder. (Implemented 2026-04-02 8:28 PM, by Selia Rena)
class CascadedChronoSpanFormatter:
    def __init__(self, scale_formatters: dict[ChronoScale, ChronoSpanFormatter], separator: str, excluded_scales: set[ChronoScale]):
        self._scale_formatters: dict[ChronoScale, ChronoSpanFormatter] = scale_formatters
        self._separator: str = separator
        self._excluded_scales: set[ChronoScale] = excluded_scales
        
    def format(self, cascaded_span: CascadedChronoSpan) -> str:
        formatted_parts = []
        
        for span in cascaded_span.inner_ordered_spans:
            if span.scale in self._excluded_scales:
                continue
            
            formatter = self._scale_formatters[span.scale]
            formatted_part = formatter[span]
            formatted_parts.append(formatted_part)
        
        return self._separator.join(formatted_parts)
    
    def __getitem__(self, cascaded_span: CascadedChronoSpan) -> str:
        return self.format(cascaded_span)
    
class CascadedChronoSpanFormatterBuilder:
    def __init__(self):
        self.scale_patterns: dict[ChronoScale, str | None] = {scale: None for scale in ChronoScale}
        self.separator: str = ""
        self.excluded_scales: set[ChronoScale] = set()
    
    def with_pattern(self, scale: ChronoScale, pattern: str):
        self.scale_patterns[scale] = pattern
        return self
    
    def with_patterns(self, patterns: dict[ChronoScale, str]):
        for scale, pattern in patterns.items():
            self.scale_patterns[scale] = pattern
        return self
    
    def with_separator(self, separator: str):
        self.separator = separator
        return self
    
    def with_excluded_scales(self, scales: set[ChronoScale]):
        self.excluded_scales |= scales
        return self
    
    def with_excluded_scale(self, scale: ChronoScale):
        self.excluded_scales.add(scale)
        return self
    
    def build(self) -> CascadedChronoSpanFormatter:
        effective_exclusions = {scale for scale, pattern in self.scale_patterns.items() if pattern is None} | self.excluded_scales
        scale_formatters = {scale: ChronoSpanFormatter().compile(pattern) for scale, pattern in self.scale_patterns.items() if scale not in effective_exclusions}
        return CascadedChronoSpanFormatter(scale_formatters, self.separator, effective_exclusions)
    
# ===== test code =====
if __name__ == "__main__":
    span = ChronoSpan(86411000, ChronoScale.SECOND)
    cascaded = CascadedChronoSpan.from_span(span)
    cascaded = cascaded.transform(CascadingType.FULL_PADDED)
    
    formatter = CascadedChronoSpanFormatterBuilder() \
        .with_pattern(ChronoScale.WEEK, "$[value] $[scalename]/$[scalelabel]") \
        .with_pattern(ChronoScale.DAY, "$[value] $[scalename]/$[scalelabel]") \
        .with_pattern(ChronoScale.HOUR, "$[value] $[scalename]/$[scalelabel]") \
        .with_pattern(ChronoScale.MINUTE, "$[value] $[scalename]/$[scalelabel]") \
        .with_pattern(ChronoScale.SECOND, "$[value] $[scalename]/$[scalelabel]") \
        .with_pattern(ChronoScale.MILLISECOND, "$[value] $[scalename]/$[scalelabel]") \
        .with_separator(", ") \
        .with_excluded_scale(ChronoScale.HOUR) \
        .with_excluded_scales({ChronoScale.MINUTE}) \
        .build()
        
    formatted = formatter[cascaded]
    print(formatted)