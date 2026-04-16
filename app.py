from src.chronica.application.engine.test_engine import TestEngine
from src.chronica.application.engine.clockheart_engine import ClockheartEngine
import time
import json
import logging

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] | [%(levelname)s] | in [%(name)s]: %(message)s",
    )
logger = logging.getLogger(__name__)

TEST_DURATION_SECONDS = 120
TICK_DURATION_S = 1

def main():
    configure_logging()
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
    logger.info(engine.debug_dump)

if __name__ == "__main__":
    main()