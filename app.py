from src.chronica.application.engine.test_engine import TestEngine
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
    logger.info("----- Starting Chronica Test Engine -----")
    engine = TestEngine()
    engine.run()
    nowtime = 0
    while nowtime < TEST_DURATION_SECONDS:
        time.sleep(TICK_DURATION_S)
        engine.tick()
        nowtime += TICK_DURATION_S
    engine.stop()
    logger.info("----- App Usage Report -----")
    logger.info(json.dumps(engine.report.to_debug_dict(), indent=4, ensure_ascii=False))
    logger.info("----- Session History -----")
    logger.info(json.dumps(engine.history.to_debug_list(), indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()