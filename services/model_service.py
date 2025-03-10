"""
Service for running and interacting with Ollama models.
"""

import json
import time
import requests
from config import (
    DEFAULT_MODEL,
    DEFAULT_TOP_K,
    DEFAULT_TOP_P,
    DEFAULT_TEMPERATURE,
    MODEL_EXECUTION_TIMEOUT,
    OLLAMA_GENERATE_ENDPOINT,
)
from utils.logging_config import setup_logger

logger = setup_logger()

def run_model(prompt, model=DEFAULT_MODEL, temperature=DEFAULT_TEMPERATURE, 
             top_k=DEFAULT_TOP_K, top_p=DEFAULT_TOP_P):
    """
    Run a model inference with the specified parameters.
    
    Args:
        prompt (str): The input prompt for the model
        model (str): The model name to use
        temperature (float): Temperature parameter for generation
        top_k (int): Top-K parameter for generation
        top_p (float): Top-P parameter for generation
        
    Yields:
        str: Generated text chunks or error messages
    """
    start_time = time.time()
    logger.info(f"Request to model: {model} | T: {temperature} | K: {top_k} | P: {top_p}")
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
        response = requests.post(OLLAMA_GENERATE_ENDPOINT, json=payload, 
                               stream=True, timeout=MODEL_EXECUTION_TIMEOUT)
        
        if response.status_code != 200:
            error_msg = f"API returned error: HTTP {response.status_code}"
            logger.error(error_msg)
            try:
                error_detail = response.json()
                logger.error(f"Error details: {error_detail}")
            except:
                logger.debug("No JSON error details available")
            yield f"Error: API returned status code {response.status_code}"
            return
            
        logger.debug("Streaming response started")
        # Stream response
        full_response = ""
        chunk_count = 0
        last_log_time = time.time()
        last_progress_log = 0
        
        for chunk in response.iter_lines():
            if chunk:
                try:
                    data = chunk.decode("utf-8")
                    if '"response":"' in data:
                        text_chunk = json.loads(data)["response"]
                        full_response += text_chunk
                        chunk_count += 1
                        
                        # Log periodically (every 1 second) to avoid console spam
                        current_time = time.time()
                        if current_time - last_log_time > 1:
                            # Calculate tokens per second
                            elapsed = current_time - start_time
                            tokens_per_sec = chunk_count / elapsed if elapsed > 0 else 0
                            
                            # Log progress every ~500 tokens or if significant progress
                            if chunk_count - last_progress_log >= 500:
                                logger.info(f"Received {chunk_count} chunks ({tokens_per_sec:.1f} tokens/sec), response length: {len(full_response)} chars")
                                last_progress_log = chunk_count
                                
                            last_log_time = current_time
                            
                        yield text_chunk
                    elif '"done":true' in data:
                        elapsed_time = time.time() - start_time
                        tokens_per_sec = chunk_count / elapsed_time if elapsed_time > 0 else 0
                        logger.success(f"Response completed in {elapsed_time:.2f}s | Length: {len(full_response)} chars | {chunk_count} chunks | {tokens_per_sec:.1f} tokens/sec")
                except json.JSONDecodeError as e:
                    logger.warning(f"JSON parse error in chunk: {str(e)}")
                    logger.debug(f"Problematic chunk data: {data[:100]}...")
                    continue
                except Exception as e:
                    logger.exception(f"Error parsing chunk: {str(e)}")
                    continue
        
    except requests.exceptions.Timeout:
        error_msg = f"Request timed out after {MODEL_EXECUTION_TIMEOUT} seconds"
        logger.error(error_msg)
        yield f"Error: {error_msg}"
    except requests.exceptions.ConnectionError:
        error_msg = "Connection error: Ollama API is not running or unreachable"
        logger.error(error_msg)
        yield f"Error: {error_msg}"
    except requests.exceptions.RequestException as e:
        logger.exception(f"Request error: {str(e)}")
        yield f"Error connecting to Ollama API: {str(e)}"
    except Exception as e:
        logger.exception(f"Unexpected error during model execution: {str(e)}")
        yield f"Unexpected error: {str(e)}"