"""
Service for running and interacting with LLM models.

This module handles model inference with streaming responses from both
Ollama and LMStudio APIs, parameter validation, and comprehensive error handling.
"""

import json
import time
import requests
from typing import Generator, Optional, Literalimport requestsfrom typing import Generator, Optional, Literalimport requests

from config import (
    MIN_TOP_K,
    MAX_TOP_K,
    MIN_TOP_P,
    MAX_TOP_P,
    DEFAULT_MODEL,
    DEFAULT_TOP_K,
    DEFAULT_TOP_P,
    MIN_TEMPERATURE,
    MAX_TEMPERATURE,
    ACTIVE_LLM_BACKEND,
    DEFAULT_TEMPERATURE,
    MODEL_EXECUTION_TIMEOUT,
    OLLAMA_GENERATE_ENDPOINT,
    LMSTUDIO_CHAT_COMPLETIONS_ENDPOINT,
)
from utils.logging_config import setup_logger

logger = setup_logger()


def validate_model_parameters(
    temperature: float = DEFAULT_TEMPERATURE,
    top_k: int = DEFAULT_TOP_K,
    top_p: float = DEFAULT_TOP_P,
) -> tuple:
    """
    Validate and clamp model parameters to acceptable ranges.
    
    Args:
        temperature: Generation temperature (0.1-1.0)
        top_k: Top-K sampling parameter (1-100)
        top_p: Top-P nucleus sampling parameter (0.0-1.0)
        
    Returns:
        tuple: Validated (temperature, top_k, top_p) parameters
        
    Raises:
        ValueError: If parameters are outside acceptable ranges after clamping
    """
    # Clamp temperature
    clamped_temperature = max(
        MIN_TEMPERATURE,
        min(MAX_TEMPERATURE, temperature)
    )
    if clamped_temperature != temperature:
        logger.warning(
            f"Temperature {temperature} clamped to {clamped_temperature}"
        )
    
    # Clamp top_k
    clamped_top_k = max(
        MIN_TOP_K,
        min(MAX_TOP_K, top_k)
    )
    if clamped_top_k != top_k:
        logger.warning(f"Top-K {top_k} clamped to {clamped_top_k}")
    
    # Clamp top_p
    clamped_top_p = max(
        MIN_TOP_P,
        min(MAX_TOP_P, top_p)
    )
    if clamped_top_p != top_p:
        logger.warning(f"Top-P {top_p} clamped to {clamped_top_p}")
    
    return clamped_temperature, clamped_top_k, clamped_top_p


def run_model(
    prompt: str,
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    top_k: int = DEFAULT_TOP_K,
    top_p: float = DEFAULT_TOP_P,
    backend: Optional[Literal["ollama", "lmstudio"]] = None,
) -> Generator[str, None, None]:
    """
    Run a model inference with the specified parameters.

    Sends a streaming request to the configured LLM backend (Ollama or LMStudio)
    and yields response tokens as they arrive. Includes comprehensive error 
    handling and logging.
    
    Args:
        prompt: The input prompt for the model
        model: The model name to use (default: from config)
        temperature: Generation temperature, 0.1-1.0 (default: from config)
        top_k: Top-K sampling parameter, 1-100 (default: from config)
        top_p: Top-P nucleus sampling parameter, 0.0-1.0 (default: from config)
        backend: LLM backend to use ("ollama" or "lmstudio"). Uses ACTIVE_LLM_BACKEND if None.
        
    Yields:
        str: Generated text chunks or error messages
        
    Raises:
        ValueError: If prompt is empty
        
    Example:
        >>> for chunk in run_model("Hello", model="neural-chat", backend="lmstudio"):
        ...     print(chunk, end="", flush=True)
    """
    # Use specified backend or default from config
    backend = backend or ACTIVE_LLM_BACKEND
    
    if backend not in ("ollama", "lmstudio"):
        error_msg = f"Invalid backend: {backend}. Must be 'ollama' or 'lmstudio'"
        logger.error(error_msg)
        yield f"Error: {error_msg}"
        return
    
    # Validate inputs
    if not prompt or not prompt.strip():
        error_msg = "Prompt cannot be empty"
        logger.error(error_msg)
        yield f"Error: {error_msg}"
        return
    
    if not model or not model.strip():
        logger.warning(f"Empty model name, using default: {DEFAULT_MODEL}")
        model = DEFAULT_MODEL
    
    # Validate and clamp parameters
    temperature, top_k, top_p = validate_model_parameters(
        temperature, top_k, top_p
    )
    
    # Route to appropriate backend
    if backend == "ollama":
        yield from _run_ollama_model(prompt, model, temperature, top_k, top_p)
    else:  # lmstudio
        yield from _run_lmstudio_model(prompt, model, temperature, top_p)


def _run_ollama_model(
    prompt: str,
    model: str,
    temperature: float,
    top_k: int,
    top_p: float,
) -> Generator[str, None, None]:
    """
    Run inference on Ollama backend.
    
    Args:
        prompt: The input prompt
        model: Model name
        temperature: Temperature parameter
        top_k: Top-K parameter
        top_p: Top-P parameter
        
    Yields:
        str: Generated text chunks or error messages
    """
    start_time = time.time()
    logger.info(
        f"[Ollama] Request to model: {model} | T: {temperature} | K: {top_k} | P: {top_p}"
    )
    logger.debug(f"Prompt length: {len(prompt)} chars")
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
        }
    }
    
    try:
        logger.debug("Sending request to Ollama API...")
        response = requests.post(
            OLLAMA_GENERATE_ENDPOINT,
            json=payload,
            stream=True,
            timeout=MODEL_EXECUTION_TIMEOUT
        )
        
        if response.status_code != 200:
            error_msg = f"API returned error: HTTP {response.status_code}"
            logger.error(error_msg)
            try:
                error_detail = response.json()
                logger.error(f"Error details: {error_detail}")
                yield f"Error: {error_detail.get('error', error_msg)}"
            except json.JSONDecodeError:
                logger.debug("No JSON error details available")
                yield f"Error: {error_msg}"
            return
        
        logger.debug("Streaming response started")
        
        # Process streaming response
        full_response = ""
        chunk_count = 0
        last_log_time = time.time()
        last_progress_log = 0
        
        for line in response.iter_lines():
            if line:
                try:
                    data = line.decode("utf-8")
                    if '"response":"' in data:
                        text_chunk = json.loads(data)["response"]
                        full_response += text_chunk
                        chunk_count += 1
                        
                        # Log periodically to avoid console spam
                        current_time = time.time()
                        if current_time - last_log_time > 1:
                            elapsed = current_time - start_time
                            tokens_per_sec = chunk_count / elapsed if elapsed > 0 else 0
                            
                            if chunk_count - last_progress_log >= 500:
                                logger.info(
                                    f"[Ollama] Received {chunk_count} chunks "
                                    f"({tokens_per_sec:.1f} tokens/sec), "
                                    f"response length: {len(full_response)} chars"
                                )
                                last_progress_log = chunk_count
                            
                            last_log_time = current_time
                        
                        yield text_chunk
                        
                    elif '"done":true' in data:
                        elapsed_time = time.time() - start_time
                        tokens_per_sec = (
                            chunk_count / elapsed_time if elapsed_time > 0 else 0
                        )
                        logger.success(
                            f"[Ollama] Response completed in {elapsed_time:.2f}s | "
                            f"Length: {len(full_response)} chars | "
                            f"{chunk_count} chunks | {tokens_per_sec:.1f} tokens/sec"
                        )
                        
                except json.JSONDecodeError as e:
                    logger.warning(f"JSON parse error in chunk: {str(e)}")
                    logger.debug(f"Problematic chunk data: {data[:100]}...")
                    continue
                except KeyError as e:
                    logger.warning(f"Missing expected key in response: {str(e)}")
                    continue
                except Exception as e:
                    logger.exception(f"Error parsing chunk: {str(e)}")
                    continue
        
    except requests.exceptions.Timeout as e:
        error_msg = (
            f"Request timed out after {MODEL_EXECUTION_TIMEOUT} seconds"
        )
        logger.error(f"{error_msg}: {str(e)}")
        yield f"Error: {error_msg}"
        
    except requests.exceptions.ConnectionError as e:
        error_msg = (
            "Connection error: Ollama API is not running or unreachable"
        )
        logger.error(f"{error_msg}: {str(e)}")
        yield f"Error: {error_msg}"
        
    except requests.exceptions.RequestException as e:
        logger.exception(f"Request error: {str(e)}")
        yield f"Error connecting to Ollama API: {str(e)}"
        
    except Exception as e:
        logger.exception(f"Unexpected error during model execution: {str(e)}")
        yield f"Unexpected error: {str(e)}"


def _run_lmstudio_model(
    prompt: str,
    model: str,
    temperature: float,
    top_p: float,
) -> Generator[str, None, None]:
    """
    Run inference on LMStudio backend using OpenAI-compatible API.
    
    Args:
        prompt: The input prompt
        model: Model name
        temperature: Temperature parameter
        top_p: Top-P parameter
        
    Yields:
        str: Generated text chunks or error messages
    """
    start_time = time.time()
    logger.info(
        f"[LMStudio] Request to model: {model} | T: {temperature} | P: {top_p}"
    )
    logger.debug(f"Prompt length: {len(prompt)} chars")
    
    # LMStudio uses OpenAI-compatible chat completions API
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "top_p": top_p,
        "stream": True,
    }
    
    try:
        logger.debug("Sending request to LMStudio API...")
        response = requests.post(
            LMSTUDIO_CHAT_COMPLETIONS_ENDPOINT,
            json=payload,
            stream=True,
            timeout=MODEL_EXECUTION_TIMEOUT
        )
        
        if response.status_code != 200:
            error_msg = f"API returned error: HTTP {response.status_code}"
            logger.error(error_msg)
            try:
                error_detail = response.json()
                logger.error(f"Error details: {error_detail}")
                yield f"Error: {error_detail.get('error', {}).get('message', error_msg)}"
            except json.JSONDecodeError:
                logger.debug("No JSON error details available")
                yield f"Error: {error_msg}"
            return
        
        logger.debug("Streaming response started")
        
        # Process streaming response (Server-Sent Events format)
        full_response = ""
        chunk_count = 0
        last_log_time = time.time()
        last_progress_log = 0
        
        for line in response.iter_lines():
            if line:
                try:
                    line_str = line.decode("utf-8").strip()
                    
                    # Skip empty lines and [DONE] marker
                    if not line_str or line_str == "data: [DONE]":
                        continue
                    
                    # Remove "data: " prefix
                    if line_str.startswith("data: "):
                        line_str = line_str[6:]
                    
                    # Parse JSON
                    data = json.loads(line_str)
                    
                    # Extract text from choice
                    if "choices" in data and len(data["choices"]) > 0:
                        delta = data["choices"][0].get("delta", {})
                        if "content" in delta:
                            text_chunk = delta["content"]
                            full_response += text_chunk
                            chunk_count += 1
                            
                            # Log periodically to avoid console spam
                            current_time = time.time()
                            if current_time - last_log_time > 1:
                                elapsed = current_time - start_time
                                tokens_per_sec = chunk_count / elapsed if elapsed > 0 else 0
                                
                                if chunk_count - last_progress_log >= 500:
                                    logger.info(
                                        f"[LMStudio] Received {chunk_count} chunks "
                                        f"({tokens_per_sec:.1f} tokens/sec), "
                                        f"response length: {len(full_response)} chars"
                                    )
                                    last_progress_log = chunk_count
                                
                                last_log_time = current_time
                            
                            yield text_chunk
                            
                except json.JSONDecodeError as e:
                    logger.warning(f"JSON parse error in chunk: {str(e)}")
                    logger.debug(f"Problematic chunk data: {line_str[:100]}...")
                    continue
                except KeyError as e:
                    logger.warning(f"Missing expected key in response: {str(e)}")
                    continue
                except Exception as e:
                    logger.exception(f"Error parsing chunk: {str(e)}")
                    continue
        
        elapsed_time = time.time() - start_time
        tokens_per_sec = chunk_count / elapsed_time if elapsed_time > 0 else 0
        logger.success(
            f"[LMStudio] Response completed in {elapsed_time:.2f}s | "
            f"Length: {len(full_response)} chars | "
            f"{chunk_count} chunks | {tokens_per_sec:.1f} tokens/sec"
        )
        
    except requests.exceptions.Timeout as e:
        error_msg = (
            f"Request timed out after {MODEL_EXECUTION_TIMEOUT} seconds"
        )
        logger.error(f"{error_msg}: {str(e)}")
        yield f"Error: {error_msg}"
        
    except requests.exceptions.ConnectionError as e:
        error_msg = (
            "Connection error: LMStudio API is not running or unreachable"
        )
        logger.error(f"{error_msg}: {str(e)}")
        yield f"Error: {error_msg}"
        
    except requests.exceptions.RequestException as e:
        logger.exception(f"Request error: {str(e)}")
        yield f"Error connecting to LMStudio API: {str(e)}"
        
    except Exception as e:
        logger.exception(f"Unexpected error during model execution: {str(e)}")
        yield f"Unexpected error: {str(e)}"

