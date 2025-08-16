import logging
from pathlib import Path

def _ensure_log_directory(base_path=None):
    """Ensure the logs directory exists."""
    root_dir = Path(__file__).resolve().parents[2]
    #project_root = Path(base_path).resolve().parents[2]
    log_directory = root_dir / "logs"
    log_directory.mkdir(parents=True, exist_ok=True)
    return log_directory

def _create_formatter ():
    """Create a standard log formatter."""
    return logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

def _create_handlers(log_directory, log_file, level):
    """Create file and console handlers."""
    
    # Set where and what is logged in file
    file_handler = logging.FileHandler(log_directory / log_file)
    file_handler.setLevel(level)
    
    # Set where and what is logged for console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Set formatting
    formatter = _create_formatter()
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    return file_handler, console_handler

def setup_logger(name, log_file, level=logging.DEBUG, base_path="logs"):
    """Function to setup a logger; only a single environment use."""
    
    # Ensure log directory exists
    log_directory = _ensure_log_directory(base_path)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Ensure no duplicate handlers exist to avoid duplicate lines in log
    if not logger.handlers:
        
        # Create file console handler
        file_handler, console_handler = _create_handlers(
            log_directory, log_file, level
        )
        
        # Add handler (info) to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger


def log_extract_success(logger, type, shape, execution_time, expected_rate):
    logger.setLevel(logging.INFO)
    logger.info(f"Data extraction successful for {type}!")
    logger.info(f"Extracted {shape[0]} rows " f"and {shape[1]} columns")
    logger.info(f"Execution time: {execution_time} seconds")

    if execution_time / shape[0] <= expected_rate:
        logger.info(
            "Execution time per row: " f"{execution_time / shape[0]} seconds"
        )
    else:
        logger.setLevel(logging.WARNING)
        logger.warning(
            f"Execution time per row exceeds {expected_rate}: "
            f"{execution_time / shape[0]} seconds"
        )