import logging

def get_logger(name: str = "test"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
    return logger