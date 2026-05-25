from src.chronica.domain.chronosystem import (
    CascadedChronoSpan,
    CascadingType
)

from src.chronica.common.formatters import (
    SIMPLISTIC,
    DIGITAL_CLOCK
)

from dataclasses import dataclass

def _to_cascaded_span(timespan: CascadedChronoSpan | int) -> CascadedChronoSpan:
    if isinstance(timespan, int):
        return CascadedChronoSpan.from_total_ms(timespan)
    elif isinstance(timespan, CascadedChronoSpan):
        return timespan

def simplistic_simplified_ms(timespan: CascadedChronoSpan | int) -> str:
    span = _to_cascaded_span(timespan)
    return SIMPLISTIC.format(span) if span.total_ms >= 1000 else "< 1s"

def digital_clock(timespan: CascadedChronoSpan | int) -> str:
    span = _to_cascaded_span(timespan)
    return DIGITAL_CLOCK.format(span.transform(CascadingType.FULL_PADDED))

@dataclass(frozen=True, slots=True)
class DigitalTimeEmphasis:
    shaded: str
    emphasized: str

def digital_clock_emphasis(timespan: CascadedChronoSpan | int) -> DigitalTimeEmphasis:
    """
    ### Separate the digital clock formatted duration (CascadedChronoSpan) into a shaded part and an emphasized part.\n
    - The emphasized part is until the highest unit of time from the given duration. \n
    - The shaded part is the rest of the duration. \n\n
    
    For example, if the given duration is 0:0:16:25:47.024 (fmt=w:d:hh:mm:ss.ms), the function returns...\n
    - Emphasized part = 16:25:47.024 (hr ~ ms) \n
    - Shaded part = 0:0: (wk ~ day + ':') \n
    
    ### Returns a DigitalTimeEmphasis object -> (shaded, emphasized)
    """

    dclock = digital_clock(timespan)
    cut_point = len(dclock)

    for i, c in enumerate(dclock):
        if c.isdigit() and c != '0':
            cut_point = i
            break

    if cut_point == len(dclock):
        return DigitalTimeEmphasis(shaded=dclock, emphasized='')

    j = cut_point - 1
    while j >= 0 and dclock[j] != ':':
        j -= 1

    shaded = dclock[:j + 1]
    emphasized = dclock[j + 1:]

    return DigitalTimeEmphasis(shaded, emphasized)