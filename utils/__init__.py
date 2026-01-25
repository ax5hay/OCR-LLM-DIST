"""
OCR-LLM Distributed Chat Utilities
"""

from utils.file_utils import (
    validate_file,
    extract_text_from_doc,
)
from utils.logging_config import setup_logger

__all__ = [
    "extract_text_from_doc",
    "validate_file",
    "setup_logger",
]
