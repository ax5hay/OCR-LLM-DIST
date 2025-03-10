"""
Logging configuration for the Local Chat application.
"""

import sys
from loguru import logger

def setup_logger():
    """
    Configure the logger with appropriate format and settings.
    """
    # Remove default logger
    logger.remove()
    
    # Add stdout handler with custom format
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True,
        backtrace=True,
        diagnose=True,
    )
    
    return logger