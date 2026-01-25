"""
Service for interacting with the Ollama API.

This module provides functions for health checks and model discovery
with comprehensive error handling and logging.
"""

import json
import requests
from typing import List, Optional
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter, Retry


from config import (
    DEFAULT_MODEL,
    HEALTH_CHECK_TIMEOUT,
    MODELS_FETCH_TIMEOUT,
    OLLAMA_MODELS_ENDPOINT,
    OLLAMA_VERSION_ENDPOINT,
)
from utils.logging_config import setup_logger

logger = setup_logger()


def _create_session() -> requests.Session:
    """
    Create a requests session with retry strategy.
    
    Returns:
        requests.Session: Session with retry configuration
    """
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def check_api_health() -> bool:
    """
    Check if the Ollama API is available and healthy.
    
    Performs a version check to verify the API is accessible and responding
    correctly. Includes automatic retries for transient failures.
    
    Returns:
        bool: True if API is healthy, False otherwise
        
    Example:
        >>> is_healthy = check_api_health()
        >>> if is_healthy:
        ...     print("API is ready!")
    """
    try:
        logger.debug("Checking Ollama API health...")
        session = _create_session()
        
        response = session.get(
            OLLAMA_VERSION_ENDPOINT,
            timeout=HEALTH_CHECK_TIMEOUT
        )
        
        if response.status_code == 200:
            try:
                version = response.json().get('version', 'unknown')
                logger.success(f"Ollama API is healthy. Version: {version}")
                return True
            except json.JSONDecodeError:
                logger.warning("API returned 200 but invalid JSON response")
                return False
        else:
            logger.error(
                f"Ollama API returned status code: {response.status_code}"
            )
            return False
            
    except requests.exceptions.ConnectionError as e:
        logger.error(
            f"Connection error: Ollama API is not running or unreachable. "
            f"Details: {str(e)}"
        )
        return False
    except requests.exceptions.Timeout as e:
        logger.error(
            f"Timeout: Ollama API did not respond within "
            f"{HEALTH_CHECK_TIMEOUT}s. Details: {str(e)}"
        )
        return False
    except requests.exceptions.RequestException as e:
        logger.exception(f"Failed to connect to Ollama API: {str(e)}")
        return False
    except Exception as e:
        logger.exception(f"Unexpected error checking API health: {str(e)}")
        return False


def get_available_models() -> List[str]:
    """
    Get a list of available models from the Ollama API.
    
    Fetches the list of models installed in Ollama and returns them.
    If an error occurs, returns a list with the default model.
    Includes automatic retries for transient failures.
    
    Returns:
        List[str]: List of available model names, or default model if error
        
    Example:
        >>> models = get_available_models()
        >>> print(f"Available models: {', '.join(models)}")
        Available models: deepseek-r1:1.5b, llama2:7b
    """
    try:
        logger.debug("Fetching available Ollama models...")
        session = _create_session()
        
        response = session.get(
            OLLAMA_MODELS_ENDPOINT,
            timeout=MODELS_FETCH_TIMEOUT
        )
        
        if response.status_code != 200:
            logger.warning(
                f"Failed to fetch models list: HTTP {response.status_code}"
            )
            return [DEFAULT_MODEL]
        
        data = response.json()
        
        if "models" not in data:
            logger.warning("API response missing 'models' key")
            return [DEFAULT_MODEL]
        
        models = [model["name"] for model in data["models"]]
        
        if not models:
            logger.warning("No models found in API response")
            return [DEFAULT_MODEL]
        
        logger.success(
            f"Found {len(models)} available models: {', '.join(models)}"
        )
        return models
        
    except requests.exceptions.ConnectionError as e:
        logger.error(
            f"Connection error fetching models: Ollama API is not running. "
            f"Details: {str(e)}"
        )
        return [DEFAULT_MODEL]
    except requests.exceptions.Timeout as e:
        logger.error(
            f"Timeout fetching models: API did not respond within "
            f"{MODELS_FETCH_TIMEOUT}s. Details: {str(e)}"
        )
        return [DEFAULT_MODEL]
    except requests.exceptions.RequestException as e:
        logger.exception(f"Request error fetching models: {str(e)}")
        return [DEFAULT_MODEL]
    except json.JSONDecodeError as e:
        logger.exception(f"JSON parse error in models response: {str(e)}")
        return [DEFAULT_MODEL]
    except KeyError as e:
        logger.error(f"Missing expected field in API response: {str(e)}")
        return [DEFAULT_MODEL]
    except Exception as e:
        logger.exception(f"Unexpected error fetching models: {str(e)}")
        return [DEFAULT_MODEL]


def validate_model_name(model_name: str) -> bool:
    """
    Validate that a model name is available.
    
    Args:
        model_name: Name of the model to validate
        
    Returns:
        bool: True if model is available, False otherwise
    """
    try:
        available_models = get_available_models()
        return model_name in available_models
    except Exception as e:
        logger.exception(f"Error validating model name: {str(e)}")
        return False
