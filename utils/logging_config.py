"""
Logging configuration for the OCR-LLM Distributed Chat application.

Provides a production-grade logging setup with colored output,
structured formatting, and comprehensive diagnostic information.
"""

import sys
from loguru import logger
from typing import Optional

from config import LOG_LEVEL


def setup_logger(
    level: Optional[str] = None,
    log_file: Optional[str] = None
):
    """
    Configure the logger with appropriate format and settings.
    
    Sets up console logging with color support and optional file logging.
    Includes full diagnostic information for debugging.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
               Defaults to LOG_LEVEL from config.
        log_file: Optional file path for logging output
        
    Returns:
        loguru.Logger: Configured logger instance
        
    Example:
        >>> logger = setup_logger(level="DEBUG")
        >>> logger.info("Application started")
        >>> logger.success("Operation completed")
    """
    # Remove default logger
    logger.remove()
    
    # Use provided level or config default
    level = level or LOG_LEVEL
    
    # Add stdout handler with custom format
    logger.add(
        sys.stdout,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
        level=level,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )
    
    # Add file handler if log_file is specified
    if log_file:
        logger.add(
            log_file,
            format=(
                "{time:YYYY-MM-DD HH:mm:ss} | "
                "{level: <8} | "
                "{name}:{function}:{line} - "
                "{message}"
            ),
            level=level,
            rotation="1 GB",  # Rotate when file reaches 1GB
            retention="7 days",  # Keep logs for 7 days
            compression="zip",  # Compress rotated logs
            backtrace=True,
            diagnose=True,
        )
        logger.info(f"File logging enabled: {log_file}")
    
    return logger
