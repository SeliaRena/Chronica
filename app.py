from src.chronica.application.engine.test_engine import TestEngine
import time
import json

TEST_DURATION_SECONDS = 5
TICK_DURATION_S = 1

def main():
    engine = TestEngine()
    engine.run()
    nowtime = 0
    while nowtime < TEST_DURATION_SECONDS:
        time.sleep(TICK_DURATION_S)
        engine.tick()
        nowtime += TICK_DURATION_S
    engine.stop()
    print(engine.history)

if __name__ == "__main__":
    print("Starting test...\n")
    main()