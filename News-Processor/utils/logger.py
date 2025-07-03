import logging
import os

def get_logger(name):
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel (logging.INFO)

    f = logging.FileHandler("logs/fetch_new_worker.log")
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s] %(message)s]')
    f.setFormatter (formatter)

    if not logger.handlers:
        logger.addHandler(f)
    
    return logger