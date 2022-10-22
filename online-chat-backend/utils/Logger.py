import sys
import threading
import time
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import shutil


def init_log():
    logger = logging.getLogger()
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(process)d - %(thread)d - %(filename)s - %(funcName)s - %(lineno)d - %('
        'message)s')
    console_handler.setFormatter(logging_format)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)


init_log()
logger = logging.getLogger()
