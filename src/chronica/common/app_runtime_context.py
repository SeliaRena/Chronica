from src.chronica.common.timestamp import TimestampContextProvider
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class AppRuntimeContext:
    ts_ctx_provider: TimestampContextProvider = field(default_factory=TimestampContextProvider)