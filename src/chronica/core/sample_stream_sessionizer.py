import src.chronica.core.foreground_context_sampler as fcs
from src.chronica.utils.foreground_context_util import ForegroundContext, same_window
from src.chronica.utils.pairwise_window import PairwiseWindow
from src.chronica.domain.session import Session
from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional

class SessionizerResultStatus(Enum):
    OP_SUCCESS = auto()
    OP_FAILED = auto()
    OP_IGNORED = auto()
    
class SessionizerErrorType(Enum):
    INPUT_REJECTED = auto()
    INVARIANT_VIOLATION = auto()
    EXCEPTION_RAISED = auto()
    
class SessionizerAction(Enum):
    WINDOW_SLIDE = auto()
    WINDOW_CLEAR = auto()
    WINDOW_FRONT_SLOT_ASSIGNMENT = auto()
    SESSIONIZATION = auto()
    
class SessionizerEvent(Enum):
    SESSION_EMITTED = auto()
    STREAM_STARTED = auto()
    STREAM_ENDED = auto()
    STREAM_INTERRUPTED = auto()
    
@dataclass(frozen=True)
class SessionizerResult:
    # Header
    status: SessionizerResultStatus = SessionizerResultStatus.OP_SUCCESS
    events: tuple[SessionizerEvent, ...] = ()
    error_type: Optional[SessionizerErrorType] = None
    performed_actions: tuple[SessionizerAction, ...] = ()
    # Body
    session: Optional[Session] = None
    # Misc
    message: Optional[str] = None

class SampleStreamSessionizer:
    def __init__(self):
        self.window = PairwiseWindow[ForegroundContext]()
        
    def _snapshot_session_from_window(self) -> Session:
        if not self.window.is_full():
            raise ValueError("Cannot snapshot session from window that is not full.")
        
        old, new = self.window.secured_full_snapshot
        
        return Session(
            start_ts_ms=old.acquired_ts_ms,
            end_ts_ms=new.acquired_ts_ms,
            app_name=old.exe_name,
            app_path=old.exe,
            window_title=old.window_title
        )
        
    def consume(self, sampler_result: fcs.SamplerResult):
        # Filter 1: Rule out samples with non-success status
        if sampler_result.status != fcs.SamplerResultStatus.SUCCESS:
            return SessionizerResult(
                status=SessionizerResultStatus.OP_FAILED,
                events=(SessionizerEvent.STREAM_INTERRUPTED,),
                error_type=SessionizerErrorType.INPUT_REJECTED,
                message=f"Received sampler result with non-success status: {sampler_result.status.name}"
            )
            
        # Filter 2: Rule out samples with no sample data
        if sampler_result.sample is None:
            return SessionizerResult(
                status=SessionizerResultStatus.OP_FAILED,
                events=(SessionizerEvent.STREAM_INTERRUPTED,),
                error_type=SessionizerErrorType.INPUT_REJECTED,
                message="Received sampler result with no sample data."
            )
        
        # case 1: Initial Sample
        if sampler_result.event == fcs.SamplerEvent.START_SAMPLING:
            if not self.window.is_empty():
                return SessionizerResult(
                    status=SessionizerResultStatus.OP_FAILED,
                    events=(SessionizerEvent.STREAM_INTERRUPTED,),
                    error_type=SessionizerErrorType.INVARIANT_VIOLATION,
                    message="Incorrect start condition inside sessionizer, context window may not have been cleared properly."
                )
            
            # Since this is the initial sample, we skip window comparison and directly add the sample to the window
            # ex. [None, None] -> [None, Sample1]
            self.window.slide_forward(sampler_result.sample)
            
            return SessionizerResult(
                events=(SessionizerEvent.STREAM_STARTED,),
                performed_actions=(SessionizerAction.WINDOW_SLIDE,),
                message="Received first sample and initialized context window."
            )
            
        # Checkpoint 1
        # Comparison now can happen because if the flow control reaches here, 
        # it 'theoratically' means the latest element in the window is not None
        # Clarification: [old, {new} <-- A SAMPLE MUST EXIST HERE NOW], front is the oldest, back is the latest
        # If not, we capture it here and deal with it as an invariant violation.
        latest_slot_in_window = self.window.appearance.second
        if latest_slot_in_window is None:
            return SessionizerResult(
                status=SessionizerResultStatus.OP_FAILED,
                events=(SessionizerEvent.STREAM_INTERRUPTED,),
                error_type=SessionizerErrorType.INVARIANT_VIOLATION,
                message="Invalid state reached when trying to compare incoming sample with context window, latest slot in window is unexpectedly None. This likely indicates a flaw in upstream logic."
            )
        
        # case 2: Terminal Sample
        if sampler_result.event == fcs.SamplerEvent.STOP_SAMPLING:
            # Roll the window to unconditionally let the last sample slide in.
            self.window.slide_forward(sampler_result.sample)
            
            # Take a snapshot (build a session) from the window before clearing it.
            terminal_session = self._snapshot_session_from_window()
            
            self.window.clear()
            
            return SessionizerResult(
                events=(
                    SessionizerEvent.SESSION_EMITTED,
                    SessionizerEvent.STREAM_ENDED
                ),
                performed_actions=(
                    SessionizerAction.SESSIONIZATION,
                    SessionizerAction.WINDOW_SLIDE,
                    SessionizerAction.WINDOW_CLEAR
                ),
                session=terminal_session,
                message="Received terminal sample, sessionized and cleared the context window."
            )
            
        # case 3: Intermediate Sample, Action on tick & Normal handling.
        if same_window(latest_slot_in_window, sampler_result.sample):
            return SessionizerResult(
                status=SessionizerResultStatus.OP_IGNORED,
                message="Received intermediate sample that belongs to the same session, no sessionization or window sliding needed."
            )
        else:
            # Diff in pairwise comparison means the continuous time-usage of 'latest_slot_in_window' has ended.
            # So roll the window to take the new sample to be the latest.
            self.window.slide_forward(sampler_result.sample)
            
            session = self._snapshot_session_from_window()
            
            return SessionizerResult(
                events=(SessionizerEvent.SESSION_EMITTED,),
                performed_actions=(
                    SessionizerAction.SESSIONIZATION,
                    SessionizerAction.WINDOW_SLIDE
                ),
                session=session,
                message="Met a diff in pairwise comparison, current window is successfully sessionized and slid forward."
            )