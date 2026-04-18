class ChronicaRuntimeError(RuntimeError):
    pass

class ForegroundContextError(ChronicaRuntimeError):
    pass

class ForegroundContextAquisitionError(ForegroundContextError):
    pass

class WindowTitleNormalizationError(ForegroundContextError):
    pass