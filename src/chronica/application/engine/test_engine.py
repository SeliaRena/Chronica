from src.chronica.core.foreground_context_sampler import ForegroundContextSampler as FCS
from src.chronica.core.sample_stream_sessionizer import SampleStreamSessionizer as SSS, SessionizerResultStatus, SessionizerEvent
from src.chronica.domain.app_usage_report import AppUsageReport
from src.chronica.domain.session_history import SessionHistory
import json

class TestEngine:
    def __init__(self):
        self.fcs = FCS()
        self.sss = SSS()
        self.report = AppUsageReport()
        self.history = SessionHistory()

    def run(self):
        # Test ForegroundContextSampler
        print("Run ForegroundContextSampler...")
        result = self.fcs.start_sampling()
        print(result)
        
        first = self.sss.consume(result)
        print(first)
        
    def stop(self):
        # Test ForegroundContextSampler
        print("Stop ForegroundContextSampler...")
        result = self.fcs.stop_sampling()
        print(result)
        
        last = self.sss.consume(result)
        print(last)
        self.report.add_session(last.session)
        self.history.append(last.session)
        
    def tick(self):
        # Test SampleStreamSessionizer
        print("Tick SampleStreamSessionizer...")
        
        sessionizer_result = self.sss.consume(self.fcs.on_tick())
        print(sessionizer_result)
        if SessionizerEvent.SESSION_EMITTED == sessionizer_result.events:
            self.report.add_session(sessionizer_result.session)
            self.history.append(sessionizer_result.session)