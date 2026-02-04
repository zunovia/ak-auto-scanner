"""
Logging configuration for the AK Auto-Scanner.
"""
import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(name: str = "kindle_scanner", log_dir: Path = None) -> logging.Logger:
    """
    Set up a logger with console and file handlers.

    Args:
        name: Logger name
        log_dir: Directory for log files (default: output/logs)

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Create formatters
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler (INFO and above)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler (DEBUG and above)
    if log_dir is None:
        log_dir = Path("output/logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / f"scanner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    logger.info(f"Logging initialized. Log file: {log_file}")

    return logger


# Default logger instance
logger = setup_logger()
