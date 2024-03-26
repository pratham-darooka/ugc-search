import logging
import os
from globals import LOG_LEVEL

def setup_logger():
    # Create a logger
    logger = logging.getLogger(__name__)

    # Set the logging level based on environment variable or default to DEBUG
    log_level = LOG_LEVEL
    numeric_level = getattr(logging, log_level.upper(), logging.DEBUG)
    logger.setLevel(numeric_level)

    # Create a console handler
    handler = logging.StreamHandler()
    handler.setLevel(numeric_level)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger

# Initialize the logger
logger = setup_logger()
