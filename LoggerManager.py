import logging
import os
from datetime import datetime

# Dictionary to store loggers for different operations
loggers = {}

def set_logger(operation_name, log_dir="Logs"):
    """
    Sets up a logger for the operation and returns it.
    Creates a new logger if one doesn't exist.
    """
    # Create a directory for logs if not exists
    os.makedirs(log_dir, exist_ok=True)

    # Create a subdirectory for each operation's logs
    operation_log_dir = os.path.join(log_dir, f"{operation_name}Logs")
    os.makedirs(operation_log_dir, exist_ok=True)

    # Create timestamped log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(operation_log_dir, f'{operation_name}_{timestamp}.log')

    # Create and configure the logger
    logger = logging.getLogger(operation_name)
    logger.setLevel(logging.INFO)  # Can be changed to DEBUG for more detailed logs

    # Check if logger already has handlers (to avoid duplicate handlers)
    if not logger.hasHandlers():
        # Create handlers for file and console logging
        file_handler = logging.FileHandler(log_file)
        console_handler = logging.StreamHandler()

        # Define the log format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


def get_logger(operation_name, log_dir="Logs"):
    """
    Gets the logger for the operation, creating it if necessary.
    """
    if operation_name not in loggers:
        # Logger not set up for this operation, so set it up
        loggers[operation_name] = set_logger(operation_name, log_dir)

    return loggers[operation_name]
