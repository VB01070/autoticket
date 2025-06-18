import logging
import os

CACHE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs", "app_logger.log"))

# create a logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)

# Only add handlers if none exist
if not logger.handlers:
    # create log file
    file_handler = logging.FileHandler(CACHE_PATH, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    # log format
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # log console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
