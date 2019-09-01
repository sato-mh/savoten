import logging
import os

DEBUG = os.getenv('DEBUG', False)


def get_logger(name):
    logger = logging.getLogger(name)
    if DEBUG:
        logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
