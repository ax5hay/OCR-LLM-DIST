"""
Utilities for document processing and text extraction.
"""

import time
import fitz  # PyMuPDF
from utils.logging_config import setup_logger

logger = setup_logger()

def extract_text_from_doc(uploaded_file):
    """
    Extract text from uploaded document (PDF or text file).
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        str: Extracted text or error message
    """
    start_time = time.time()
    logger.info(f"Processing document: {uploaded_file.name} ({uploaded_file.type})")
    
    text = ""
    try:
        if uploaded_file.type == "application/pdf":
            text = _process_pdf(uploaded_file)
        else:
            text = _process_text_file(uploaded_file)
        
        elapsed_time = time.time() - start_time
        logger.success(f"Document extraction completed in {elapsed_time:.2f}s | Extracted {len(text)} chars")
        return text
    except Exception as e:
        logger.exception(f"Unexpected error extracting text: {str(e)}")
        return f"Error extracting text: {str(e)}"

def _process_pdf(uploaded_file):
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
        
        # Open PDF with PyMuPDF
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        page_count = len(doc)
        logger.info(f"PDF has {page_count} pages")
        
        text = ""
        for i, page in enumerate(doc):
            try:
                page_text = page.get_text()
                text += page_text
                # Log progress at appropriate intervals
                log_interval = max(1, min(5, page_count // 10))  # Adaptive logging
                if i % log_interval == 0 or i == page_count - 1:
                    logger.debug(f"Processed page {i+1}/{page_count}")
            except Exception as e:
                logger.error(f"Error extracting text from page {i+1}: {str(e)}")
                text += f"\n[Error extracting text from page {i+1}]\n"
        
        logger.debug(f"Successfully extracted text from all {page_count} pages")
        return text
    except fitz.FileDataError as e:
        logger.error(f"PDF parsing error: {str(e)}")
        return f"Error: Could not parse PDF file. The file may be corrupted or password-protected."
    except Exception as e:
        logger.exception(f"Error processing PDF: {str(e)}")
        return f"Error processing PDF: {str(e)}"

def _process_text_file(uploaded_file):
    """
    Process text file and extract content.
    
    Args:
        uploaded_file: Streamlit uploaded text file
        
    Returns:
        str: Extracted text or error message
    """
    try:
        file_bytes = uploaded_file.read()
        text = file_bytes.decode("utf-8")
        logger.info(f"Processed text file ({len(text)} chars)")
        return text
    except UnicodeDecodeError as e:
        logger.error(f"Text encoding error: {str(e)}")
        # Try alternative encodings
        for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
            try:
                logger.debug(f"Trying alternative encoding: {encoding}")
                text = file_bytes.decode(encoding)
                logger.success(f"Successfully decoded with {encoding} encoding")
                return text
            except UnicodeDecodeError:
                continue
        
        return "Error: Could not decode text file with any supported encoding."
    except Exception as e:
        logger.exception(f"Error processing text file: {str(e)}")
        return f"Error processing text file: {str(e)}"