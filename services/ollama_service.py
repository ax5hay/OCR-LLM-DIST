"""
Service for interacting with the Ollama API.
"""

import json
import requests
from config import (
    DEFAULT_MODEL,
    HEALTH_CHECK_TIMEOUT,
    MODELS_FETCH_TIMEOUT,
    OLLAMA_MODELS_ENDPOINT,
    OLLAMA_VERSION_ENDPOINT,
)
from utils.logging_config import setup_logger

logger = setup_logger()

def check_api_health():
    """
    Check if the Ollama API is available and healthy.
    
    Returns:
        bool: True if API is healthy, False otherwise
    """
    try:
        logger.debug("Checking Ollama API health...")
        response = requests.get(OLLAMA_VERSION_ENDPOINT, timeout=HEALTH_CHECK_TIMEOUT)
        if response.status_code == 200:
            version = response.json().get('version', 'unknown')
            logger.success(f"Ollama API is healthy. Version: {version}")
            return True
        else:
            logger.error(f"Ollama API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        logger.error("Connection error: Ollama API is not running or unreachable")
        return False
    except requests.exceptions.Timeout:
        logger.error("Timeout: Ollama API did not respond within the timeout period")
        return False
    except requests.exceptions.RequestException as e:
        logger.exception(f"Failed to connect to Ollama API: {str(e)}")
        return False
    except Exception as e:
        logger.exception(f"Unexpected error checking API health: {str(e)}")
        return False

def get_available_models():
    """
    Get a list of available models from the Ollama API.
    
    Returns:
        list: List of available model names, or default model if error
    """
    try:
        logger.debug("Fetching available Ollama models...")
        response = requests.get(OLLAMA_MODELS_ENDPOINT, timeout=MODELS_FETCH_TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            if "models" not in data:
                logger.warning("API response missing 'models' key")
                return [DEFAULT_MODEL]
                
            models = [model["name"] for model in data["models"]]
            if not models:
                logger.warning("No models found in API response")
                return [DEFAULT_MODEL]
                
            logger.success(f"Found {len(models)} available models: {', '.join(models)}")
            return models
        else:
            logger.warning(f"Failed to fetch models list: HTTP {response.status_code}")
            return [DEFAULT_MODEL]
    except requests.exceptions.ConnectionError:
        logger.error("Connection error fetching models: Ollama API is not running or unreachable")
        return [DEFAULT_MODEL]
    except requests.exceptions.Timeout:
        logger.error("Timeout fetching models: API did not respond within the timeout period")
        return [DEFAULT_MODEL]
    except requests.exceptions.RequestException as e:
        logger.exception(f"Request error fetching models: {str(e)}")
        return [DEFAULT_MODEL]
    except json.JSONDecodeError as e:
        logger.exception(f"JSON parse error in models response: {str(e)}")
        return [DEFAULT_MODEL]
    except Exception as e:
        logger.exception(f"Unexpected error fetching models: {str(e)}")
        return [DEFAULT_MODEL]