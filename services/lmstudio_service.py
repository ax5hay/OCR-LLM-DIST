"""
Service for interacting with LMStudio API.

This module provides functions for health checks and model discovery
with the OpenAI-compatible LMStudio API endpoints.
"""

import json
import requests
from typing import List, Optional
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter, Retry

from config import (
    DEFAULT_MODEL,
    LMSTUDIO_API_BASE,
    LMSTUDIO_MODELS_ENDPOINT,
    LMSTUDIO_CHAT_COMPLETIONS_ENDPOINT,
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
    Check if the LMStudio API is available and healthy.
    
    Performs a models list check to verify the API is accessible and responding
    correctly. Includes automatic retries for transient failures.
    
    Returns:
        bool: True if API is healthy, False otherwise
        
    Example:
        >>> is_healthy = check_api_health()
        >>> if is_healthy:
        ...     print("LMStudio API is ready!")
    """
    try:
        logger.debug("Checking LMStudio API health...")
        session = _create_session()
        
        response = session.get(
            LMSTUDIO_MODELS_ENDPOINT,
            timeout=5
        )
        
        if response.status_code == 200:
            try:
                data = response.json()
                if "data" in data:
                    logger.success(f"LMStudio API is healthy")
                    return True
            except json.JSONDecodeError:
                logger.warning("API returned 200 but invalid JSON response")
                return False
        else:
            logger.error(
                f"LMStudio API returned status code: {response.status_code}"
            )
            return False
            
    except requests.exceptions.ConnectionError as e:
        logger.error(
            f"Connection error: LMStudio API is not running or unreachable. "
            f"Ensure LMStudio is running on {LMSTUDIO_API_BASE}"
        )
        return False
    except requests.exceptions.Timeout as e:
        logger.error(
            f"Timeout: LMStudio API did not respond. Details: {str(e)}"
        )
        return False
    except requests.exceptions.RequestException as e:
        logger.exception(f"Failed to connect to LMStudio API: {str(e)}")
        return False
    except Exception as e:
        logger.exception(f"Unexpected error checking API health: {str(e)}")
        return False


def get_available_models() -> List[str]:
    """
    Get a list of available models from the LMStudio API.
    
    Fetches the list of models loaded in LMStudio and returns them.
    If an error occurs, returns a list with the default model.
    Includes automatic retries for transient failures.
    
    Returns:
        List[str]: List of available model names, or default model if error
        
    Example:
        >>> models = get_available_models()
        >>> print(f"Available models: {', '.join(models)}")
        Available models: neural-chat:latest, llama2:7b
    """
    try:
        logger.debug("Fetching available LMStudio models...")
        session = _create_session()
        
        response = session.get(
            LMSTUDIO_MODELS_ENDPOINT,
            timeout=10
        )
        
        if response.status_code != 200:
            logger.warning(
                f"Failed to fetch models list: HTTP {response.status_code}"
            )
            return [DEFAULT_MODEL]
        
        data = response.json()
        
        if "data" not in data:
            logger.warning("API response missing 'data' key")
            return [DEFAULT_MODEL]
        
        models = [model.get("id", model) for model in data["data"]]
        
        if not models:
            logger.warning("No models found in API response")
            return [DEFAULT_MODEL]
        
        logger.success(
            f"Found {len(models)} available models: {', '.join(models)}"
        )
        return models
        
    except requests.exceptions.ConnectionError as e:
        logger.error(
            f"Connection error fetching models: LMStudio API is not running. "
            f"Details: {str(e)}"
        )
        return [DEFAULT_MODEL]
    except requests.exceptions.Timeout as e:
        logger.error(
            f"Timeout fetching models: API did not respond. Details: {str(e)}"
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
        bool: True if model exists, False otherwise
    """
    try:
        available_models = get_available_models()
        return model_name in available_models
    except Exception as e:
        logger.exception(f"Error validating model name: {str(e)}")
        return False
