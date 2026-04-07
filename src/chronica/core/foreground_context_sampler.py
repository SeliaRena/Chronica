import src.chronica.utils.time_util as time_util
import src.chronica.utils.foreground_context_util as foreground_context_util
from enum import Enum, auto
from typing import Optional
from dataclasses import dataclass

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
    emitted_ts_ms: int = time_util.get_current_unix_timestamp_ms()
    sample: Optional[foreground_context_util.ForegroundContext] = None
    state: SamplerState
    event: Optional[SamplerEvent] = None
    status: SamplerResultStatus = SamplerResultStatus.SUCCESS
    message: Optional[str] = None

class ForegroundContextSampler:
    """
    ### A class used to sample the foreground context of your window device repeatedly within a certain interval. \n
    
    A sample is taken on each tick when the sampler is in the SAMPLING state and the sampling frequency is determined
    by the tick frequency of the qTimer in the main application. \n
    
    <i><b> context_data </b></i> is left here for extension, it can be used to store sampled context data if needed.
    """
    
    def __init__(self):
        self.state = SamplerState.IDLE
        self.context_data = None # left here for extension, can be used to store sampled context data
        
    def start_sampling(self) -> SamplerResult:
        if self.state == SamplerState.SAMPLING:
            return SamplerResult(
                state=self.state,
                status=SamplerResultStatus.ERROR_ALREADY_RUNNING
            )
        self.state = SamplerState.SAMPLING
        return SamplerResult(
            state=self.state,
            event=SamplerEvent.START_SAMPLING,
            message="Sampler started successfully."
        )
            
    def stop_sampling(self) -> SamplerResult:
        if self.state == SamplerState.IDLE:
            return SamplerResult(
                state=self.state,
                status=SamplerResultStatus.ERROR_ALREADY_STOPPED
            )
        self.state = SamplerState.IDLE
        return SamplerResult(
            sample=foreground_context_util.get_foreground_context(),
            state=self.state,
            event=SamplerEvent.STOP_SAMPLING,
            message="Sampler stopped successfully. Sent a terminal sample of the foreground context at the time of stopping."
        )
            
    def on_tick(self) -> SamplerResult:
        if self.state == SamplerState.IDLE:
            return SamplerResult(
                state=self.state,
                status=SamplerResultStatus.ERROR_SAMPLING_FAILED,
                message="Tried to sample while in IDLE state."
            )
        sample = foreground_context_util.get_foreground_context()
        return SamplerResult(
            sample=sample,
            state=self.state
        )
    
    pass