import re
from enum import Enum, auto
from collections.abc import Iterable, Callable

_TRANSIENT_NOTIFICATION_TAG_REGEX = re.compile(r'(?:\s*[\(\[]\d+\+?[\)\]])+')

class TransientMarkerType(Enum):
    NOTIFICATION_TAG = auto()
    
_TRANSIENT_MARKER_ERASE_RULES: dict[TransientMarkerType, re.Pattern] = {
    TransientMarkerType.NOTIFICATION_TAG: _TRANSIENT_NOTIFICATION_TAG_REGEX
}

def _erase_transient_markers(title: str, marker_types: Iterable[TransientMarkerType]) -> str:
    for marker_type in marker_types:
        rule = _TRANSIENT_MARKER_ERASE_RULES.get(marker_type)
        if rule is not None:
            title = rule.sub('', title)
    return title.strip()

class SimpleNormalizationOption(Enum):
    COLLAPSE_WHITESPACE = auto()

def _collapse_whitespace(title: str) -> str:
    return re.sub(r'\s+', ' ', title).strip()

_SIMPLE_NORMALIZATION_RULES: dict[SimpleNormalizationOption, Callable[[str], str]] = {
    SimpleNormalizationOption.COLLAPSE_WHITESPACE: _collapse_whitespace
}

class WindowTitleNormalizer:
    def __init__(self, transient_marker_types: Iterable[TransientMarkerType] = (), simple_normalization_options: Iterable[SimpleNormalizationOption] = ()):
        self.transient_marker_types = tuple(dict.fromkeys(transient_marker_types))
        self.simple_normalization_options = tuple(dict.fromkeys(simple_normalization_options))
    
    def normalize(self, title: str) -> str:
        title = _erase_transient_markers(title, self.transient_marker_types)
        for option in self.simple_normalization_options:
            title = _SIMPLE_NORMALIZATION_RULES[option](title)
        return title.strip()
    
DEFAULT_NORMALIZER = WindowTitleNormalizer(
    transient_marker_types=[TransientMarkerType.NOTIFICATION_TAG],
    simple_normalization_options=[SimpleNormalizationOption.COLLAPSE_WHITESPACE]
)