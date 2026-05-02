from src.chronica.utils.foreground_context_util import ForegroundContext, get_foreground_context
from src.chronica.common.errors import ForegroundContextError
from enum import Enum, auto
from dataclasses import dataclass, field, asdict
import src.chronica.common.timestamp as timestamp

class SamplerState(Enum):
    IDLE = auto()
    SAMPLING = auto()

class SamplerEvent(Enum):
    START_SAMPLING = auto()
    STOP_SAMPLING = auto()

class SamplerResultStatus(Enum):
    SUCCESS = auto()
    ERROR_ALREADY_RUNNING = auto()
    ERROR_ALREADY_STOPPED = auto()
    ERROR_SAMPLING_FAILED = auto()
    EXTERNAL_ERROR = auto()

@dataclass(frozen=True)
class SamplerResult:
    state: SamplerState
    emitted_ts_ms: int = field(default_factory=timestamp.now_ts_ms)
    sample: ForegroundContext | None = None
    event: SamplerEvent | None = None
    status: SamplerResultStatus = SamplerResultStatus.SUCCESS
    error_class: str | None = None
    message: str | None = None
    
    def to_debug_dict(self) -> dict:
        return {
            "state": self.state.name,
            "emitted_ts_ms": self.emitted_ts_ms,
            "sample": asdict(self.sample) if self.sample else None,
            "event": self.event.name if self.event else None,
            "status": self.status.name,
            "error_class": self.error_class,
            "message": self.message
        }

class ForegroundContextSampler:
    """
    ### A class used to sample the foreground context of your window device repeatedly within a certain interval. \n
    
    A sample is taken on each tick when the sampler is in the SAMPLING state and the sampling frequency is determined
    by the tick frequency of the qTimer in the main application. \n
    """
    
    def __init__(self):
        self.state = SamplerState.IDLE
        self.latest_sample: ForegroundContext | None = None
        
    def _try_acquire_sample(self, *, event: SamplerEvent | None = None, success_message: str | None = None) -> SamplerResult:
        try:
            sample = get_foreground_context()
            return SamplerResult(
                state=self.state,
                sample=sample,
                event=event,
                message=success_message
            )
        except ForegroundContextError as e:
            return SamplerResult(
                state=self.state,
                status=SamplerResultStatus.EXTERNAL_ERROR,
                error_class=type(e).__name__,
                message=f"Failed to acquire foreground context sample: {e}"
            )

    def reset(self) -> None:
        self.state = SamplerState.IDLE
        self.latest_sample = None

    def start_sampling(self) -> SamplerResult:
        if self.state == SamplerState.SAMPLING:
            return SamplerResult(
                state=self.state,
                status=SamplerResultStatus.ERROR_ALREADY_RUNNING
            )
        self.state = SamplerState.SAMPLING
        
        initial_result = self._try_acquire_sample(
            event=SamplerEvent.START_SAMPLING,
            success_message="Sampler started successfully and emitted an initial sample."
        )
        self.latest_sample = initial_result.sample
        return initial_result
            
    def stop_sampling(self) -> SamplerResult:
        if self.state == SamplerState.IDLE:
            return SamplerResult(
                state=self.state,
                status=SamplerResultStatus.ERROR_ALREADY_STOPPED
            )
        self.state = SamplerState.IDLE
        
        terminal_result = self._try_acquire_sample(
            event=SamplerEvent.STOP_SAMPLING,
            success_message="Sampler stopped successfully and emitted a terminal sample."
        )
        self.latest_sample = terminal_result.sample
        return terminal_result
            
    def on_tick(self) -> SamplerResult:
        if self.state == SamplerState.IDLE:
            return SamplerResult(
                state=self.state,
                status=SamplerResultStatus.ERROR_SAMPLING_FAILED,
                message="Tried to sample while in IDLE state."
            )
            
        result = self._try_acquire_sample()
        self.latest_sample = result.sample
        return result