from src.chronica.application.engine.clockheart_engine import ClockheartEngine
from src.chronica.infra.logging.logging_config import setup_runtime_logger
from src.chronica.infra.report.report_writer import write_report
from src.chronica.ui.main_window import ChronicaMainWindow
from src.chronica.ui.controllers.runtime_controller import RuntimeController
from PySide6.QtWidgets import QApplication
import time
import logging

logger = logging.getLogger(__name__)

TEST_DURATION_SECONDS = 120
TICK_DURATION_S = 1

def main():
    setup_runtime_logger()
    
    logger.info("----- Starting Chronica Clockheart Engine Execution -----")
    engine = ClockheartEngine()
    engine.start()
    nowtime = 0
    while nowtime < TEST_DURATION_SECONDS:
        time.sleep(TICK_DURATION_S)
        engine.tick()
        nowtime += TICK_DURATION_S
    engine.stop()
    logger.info("----- Chronica Clockheart Engine Execution Finished -----")
    
    write_report(engine.debug_dump)
    
def run_gui() -> int:
    setup_runtime_logger()
    
    app = QApplication([])
    window = ChronicaMainWindow()
    engine = ClockheartEngine()
    controller = RuntimeController(window, engine)
    
    window.show()
    return app.exec()

if __name__ == "__main__":
    raise SystemExit(run_gui())