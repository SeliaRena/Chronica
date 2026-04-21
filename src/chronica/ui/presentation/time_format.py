from src.chronica.domain.chronosystem import CascadedChronoSpan
from src.chronica.common.formatters import SIMPLISTIC

def simplistic_simplified_ms(total_ms: int) -> str:
    return SIMPLISTIC.format(CascadedChronoSpan.from_total_ms(total_ms)) if total_ms >= 1000 else "< 1s"