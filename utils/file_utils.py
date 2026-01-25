"""
Utilities for document processing and text extraction.

This module provides functionality for extracting text from various
document formats (PDF, TXT) with comprehensive error handling.
"""

import time
import fitz  # PyMuPDF
from typing import Optional

from utils.logging_config import setup_logger
from config import SUPPORTED_FILE_EXTENSIONS, SUPPORTED_DOCUMENT_TYPESfrom utils.logging_config import setup_loggerfrom config import SUPPORTED_FILE_EXTENSIONS, SUPPORTED_DOCUMENT_TYPESfrom utils.logging_config import setup_logger

logger = setup_logger()


def extract_text_from_doc(uploaded_file) -> str:
    """
    Extract text from uploaded document (PDF or text file).
    
    Supports PDF and plain text files with automatic encoding detection.
    Includes comprehensive error handling and detailed logging.
    
    Args:
        uploaded_file: Streamlit uploaded file object with attributes:
            - name (str): Filename
            - type (str): MIME type
            - read() method: Returns file bytes
        
    Returns:
        str: Extracted text or error message
        
    Raises:
        ValueError: If file format is not supported
        
    Example:
        >>> text = extract_text_from_doc(uploaded_file)
        >>> print(f"Extracted {len(text)} characters")
    """
    start_time = time.time()
    
    # Validate file attributes
    if not hasattr(uploaded_file, 'name') or not hasattr(uploaded_file, 'type'):
        error_msg = "Invalid file object: missing required attributes"
        logger.error(error_msg)
        return f"Error: {error_msg}"
    
    logger.info(
        f"Processing document: {uploaded_file.name} ({uploaded_file.type})"
    )
    
    # Validate file format
    if uploaded_file.type not in SUPPORTED_DOCUMENT_TYPES:
        error_msg = (
            f"Unsupported file format: {uploaded_file.type}. "
            f"Supported formats: {', '.join(SUPPORTED_DOCUMENT_TYPES)}"
        )
        logger.error(error_msg)
        return f"Error: {error_msg}"
    
    text = ""
    try:
        if uploaded_file.type == "application/pdf":
            text = _process_pdf(uploaded_file)
        else:
            # Handle text files
            text = _process_text_file(uploaded_file)
        
        elapsed_time = time.time() - start_time
        logger.success(
            f"Document extraction completed in {elapsed_time:.2f}s | "
            f"Extracted {len(text)} chars"
        )
        return text
        
    except Exception as e:
        logger.exception(f"Unexpected error extracting text: {str(e)}")
        return f"Error extracting text: {str(e)}"


def _process_pdf(uploaded_file) -> str:
    """
    Process PDF file and extract text.
    
    Args:
        uploaded_file: Streamlit uploaded PDF file
        
    Returns:
        str: Extracted text or error message
    """
    try:
        # Read file to bytes
        file_bytes = uploaded_file.read()
        logger.debug(f"Read {len(file_bytes)} bytes from file")
        
        # Validate file size
        if len(file_bytes) == 0:
            raise ValueError("Uploaded file is empty")
        
        # Open PDF with PyMuPDF
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        page_count = len(doc)
        logger.info(f"PDF has {page_count} pages")
        
        if page_count == 0:
            logger.warning("PDF has no pages")
            return ""
        
        text = ""
        for i, page in enumerate(doc):
            try:
                page_text = page.get_text()
                text += page_text
                
                # Log progress at appropriate intervals
                log_interval = max(1, min(5, page_count // 10))
                if i % log_interval == 0 or i == page_count - 1:
                    logger.debug(f"Processed page {i+1}/{page_count}")
                    
            except Exception as e:
                logger.error(f"Error extracting text from page {i+1}: {str(e)}")
                text += f"\n[Error extracting text from page {i+1}]\n"
        
        logger.debug(f"Successfully extracted text from all {page_count} pages")
        return text
        
    except fitz.FileDataError as e:
        error_msg = (
            "PDF parsing error: Could not parse PDF file. "
            "The file may be corrupted or password-protected."
        )
        logger.error(f"{error_msg}: {str(e)}")
        return f"Error: {error_msg}"
        
    except ValueError as e:
        error_msg = f"Invalid PDF file: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"
        
    except Exception as e:
        logger.exception(f"Error processing PDF: {str(e)}")
        return f"Error processing PDF: {str(e)}"


def _process_text_file(uploaded_file) -> str:
    """
    Process text file and extract content.
    
    Attempts to decode the file using UTF-8 first, then falls back
    to alternative encodings if needed.
    
    Args:
        uploaded_file: Streamlit uploaded text file
        
    Returns:
        str: Extracted text or error message
    """
    try:
        file_bytes = uploaded_file.read()
        
        if len(file_bytes) == 0:
            logger.warning("Text file is empty")
            return ""
        
        # Try UTF-8 first (most common)
        try:
            text = file_bytes.decode("utf-8")
            logger.info(f"Processed text file ({len(text)} chars) with UTF-8")
            return text
        except UnicodeDecodeError:
            logger.debug("UTF-8 decoding failed, trying alternative encodings")
        
        # Try alternative encodings
        fallback_encodings = ['latin-1', 'cp1252', 'iso-8859-1', 'utf-16']
        
        for encoding in fallback_encodings:
            try:
                logger.debug(f"Trying alternative encoding: {encoding}")
                text = file_bytes.decode(encoding)
                logger.success(
                    f"Successfully decoded text file with {encoding} encoding"
                )
                return text
            except (UnicodeDecodeError, LookupError):
                continue
        
        error_msg = (
            "Could not decode text file with any supported encoding. "
            f"Tried: UTF-8, {', '.join(fallback_encodings)}"
        )
        logger.error(error_msg)
        return f"Error: {error_msg}"
        
    except Exception as e:
        logger.exception(f"Error processing text file: {str(e)}")
        return f"Error processing text file: {str(e)}"


def validate_file(uploaded_file) -> tuple[bool, Optional[str]]:
    """
    Validate an uploaded file.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        tuple: (is_valid, error_message)
            - is_valid: True if file is valid
            - error_message: None if valid, error string otherwise
    """
    if not uploaded_file:
        return False, "No file uploaded"
    
    if not hasattr(uploaded_file, 'name'):
        return False, "Invalid file object"
    
    # Check file extension
    file_name = uploaded_file.name.lower()
    extension = file_name.split('.')[-1] if '.' in file_name else ""
    
    if extension not in SUPPORTED_FILE_EXTENSIONS:
        return (
            False,
            f"Unsupported file type: {extension}. "
            f"Supported types: {', '.join(SUPPORTED_FILE_EXTENSIONS)}"
        )
    
    # Check MIME type if available
    if hasattr(uploaded_file, 'type'):
        if uploaded_file.type not in SUPPORTED_DOCUMENT_TYPES:
            return (
                False,
                f"Unsupported MIME type: {uploaded_file.type}"
            )
    
    return True, None
