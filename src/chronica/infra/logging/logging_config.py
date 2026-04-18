import logging
import src.chronica.common.paths as paths
from datetime import datetime

def setup_runtime_logger() -> logging.Logger:
    log_dir = paths.LOGS_DIR
    log_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = log_dir / f"chronica_{timestamp}.log"
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    
    if logger.handlers:
        return logger
    
    formatter = logging.Formatter("[%(asctime)s] | [%(levelname)s] | in [%(name)s]: %(message)s")
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger