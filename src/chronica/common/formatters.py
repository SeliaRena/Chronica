from src.chronica.domain.chronosystem import ChronoScale, CascadedChronoSpanFormatter, CascadedChronoSpanFormatterBuilder

DIGITAL_CLOCK: CascadedChronoSpanFormatter = CascadedChronoSpanFormatterBuilder() \
    .with_patterns({
        ChronoScale.WEEK: "$[value].pad(1, 0)",
        ChronoScale.DAY: ":$[value].pad(1, 0)",
        ChronoScale.HOUR: ":$[value].pad(2, 0)",
        ChronoScale.MINUTE: ":$[value].pad(2, 0)",
        ChronoScale.SECOND: ":$[value].pad(2, 0)",
        ChronoScale.MILLISECOND: ".$[value].pad(3, 0)"
    }) \
    .with_separator("") \
    .build()
    
HUMAN_READABLE: CascadedChronoSpanFormatter = CascadedChronoSpanFormatterBuilder() \
    .with_patterns({
        ChronoScale.WEEK: "$[value] week(s)",
        ChronoScale.DAY: "$[value] day(s)",
        ChronoScale.HOUR: "$[value] hour(s)",
        ChronoScale.MINUTE: "$[value] minute(s)",
        ChronoScale.SECOND: "$[value] second(s)",
        ChronoScale.MILLISECOND: "$[value] millisecond(s)"
    }) \
    .with_separator(", ") \
    .build()