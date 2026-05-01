from src.chronica.domain.chronosystem import CascadedChronoSpan
from src.chronica.common.formatters import SIMPLISTIC

def simplistic_simplified_ms(timespan: CascadedChronoSpan | int) -> str:
    span = None

    if isinstance(timespan, int):
        span = CascadedChronoSpan.from_total_ms(timespan)
    elif isinstance(timespan, CascadedChronoSpan):
        span = timespan

    return SIMPLISTIC.format(span) if span.total_ms >= 1000 else "< 1s"