"""
Configuration settings for the OCR-LLM Distributed Chat application.

This module handles all application configuration through environment variables
with sensible defaults. It supports both .env files and environment variables.

Configuration Priority:
    1. Environment variables (highest)
    2. .env file
    3. Hardcoded defaults (lowest)
"""

import os
from typing import Final
from pathlib import Path

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        load_dotenv(env_file)
except ImportError:
    # dotenv not installed, skip loading from file
    pass


# ============================================
# LLM BACKEND SELECTION
# ============================================

ACTIVE_LLM_BACKEND: Final[str] = os.getenv(
    "ACTIVE_LLM_BACKEND",
    "ollama"  # Options: "ollama" or "lmstudio"
)
"""Active LLM backend: 'ollama' or 'lmstudio'"""


# ============================================
# OLLAMA API CONFIGURATION
# ============================================

OLLAMA_API_BASE: Final[str] = os.getenv(
    "OLLAMA_API_BASE",
    "http://localhost:11434"
)
"""Base URL for Ollama API service"""

OLLAMA_GENERATE_ENDPOINT: Final[str] = os.getenv(
    "OLLAMA_GENERATE_ENDPOINT",
    f"{OLLAMA_API_BASE}/api/generate"
)
"""Endpoint for text generation requests"""

OLLAMA_MODELS_ENDPOINT: Final[str] = os.getenv(
    "OLLAMA_MODELS_ENDPOINT",
    f"{OLLAMA_API_BASE}/api/tags"
)
"""Endpoint for fetching available models"""

OLLAMA_VERSION_ENDPOINT: Final[str] = os.getenv(
    "OLLAMA_VERSION_ENDPOINT",
    f"{OLLAMA_API_BASE}/api/version"
)
"""Endpoint for API version and health check"""


# ============================================
# LMSTUDIO API CONFIGURATION
# ============================================

LMSTUDIO_API_BASE: Final[str] = os.getenv(
    "LMSTUDIO_API_BASE",
    "http://127.0.0.1:1234"
)
"""Base URL for LMStudio API service"""

LMSTUDIO_MODELS_ENDPOINT: Final[str] = os.getenv(
    "LMSTUDIO_MODELS_ENDPOINT",
    f"{LMSTUDIO_API_BASE}/v1/models"
)
"""Endpoint for fetching available models"""

LMSTUDIO_CHAT_COMPLETIONS_ENDPOINT: Final[str] = os.getenv(
    "LMSTUDIO_CHAT_COMPLETIONS_ENDPOINT",
    f"{LMSTUDIO_API_BASE}/v1/chat/completions"
)
"""Endpoint for chat completions (OpenAI-compatible)"""

LMSTUDIO_COMPLETIONS_ENDPOINT: Final[str] = os.getenv(
    "LMSTUDIO_COMPLETIONS_ENDPOINT",
    f"{LMSTUDIO_API_BASE}/v1/completions"
)
"""Endpoint for text completions"""


# ============================================
# MODEL CONFIGURATION
# ============================================

DEFAULT_MODEL: Final[str] = os.getenv(
    "DEFAULT_MODEL",
    "deepseek-r1:1.5b"
)
"""Default LLM model to use for inference"""

DEFAULT_TEMPERATURE: Final[float] = float(os.getenv(
    "DEFAULT_TEMPERATURE",
    "0.7"
))
"""Default temperature for model generation (0.0-1.0)"""

DEFAULT_TOP_K: Final[int] = int(os.getenv(
    "DEFAULT_TOP_K",
    "40"
))
"""Default top-k parameter for token selection (1-100)"""

DEFAULT_TOP_P: Final[float] = float(os.getenv(
    "DEFAULT_TOP_P",
    "0.9"
))
"""Default top-p parameter for nucleus sampling (0.0-1.0)"""


# ============================================
# REQUEST TIMEOUTS (seconds)
# ============================================

HEALTH_CHECK_TIMEOUT: Final[int] = int(os.getenv(
    "HEALTH_CHECK_TIMEOUT",
    "5"
))
"""Timeout for API health checks"""

MODELS_FETCH_TIMEOUT: Final[int] = int(os.getenv(
    "MODELS_FETCH_TIMEOUT",
    "10"
))
"""Timeout for fetching available models"""

MODEL_EXECUTION_TIMEOUT: Final[int] = int(os.getenv(
    "MODEL_EXECUTION_TIMEOUT",
    "60"
))
"""Timeout for model inference execution"""


# ============================================
# CACHE SETTINGS
# ============================================

MODELS_CACHE_TTL: Final[int] = int(os.getenv(
    "MODELS_CACHE_TTL",
    "3600"
))
"""Time-to-live for cached models list (seconds)"""


# ============================================
# APPLICATION SETTINGS
# ============================================

PAGE_TITLE: Final[str] = os.getenv(
    "PAGE_TITLE",
    "Chat with Local AI"
)
"""Browser page title"""

PAGE_ICON: Final[str] = os.getenv(
    "PAGE_ICON",
    "🧠"
)
"""Browser page icon/emoji"""

LOG_LEVEL: Final[str] = os.getenv(
    "LOG_LEVEL",
    "INFO"
)
"""Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"""

ENABLE_CORS: Final[bool] = os.getenv(
    "ENABLE_CORS",
    "true"
).lower() == "true"
"""Enable CORS for cross-origin requests"""


# ============================================
# VALIDATION CONSTRAINTS
# ============================================

# Temperature constraints
MIN_TEMPERATURE: Final[float] = 0.1
"""Minimum allowed temperature value"""

MAX_TEMPERATURE: Final[float] = 1.0
"""Maximum allowed temperature value"""

# Top-K constraints
MIN_TOP_K: Final[int] = 1
"""Minimum allowed top-k value"""

MAX_TOP_K: Final[int] = 100
"""Maximum allowed top-k value"""

# Top-P constraints
MIN_TOP_P: Final[float] = 0.0
"""Minimum allowed top-p value"""

MAX_TOP_P: Final[float] = 1.0
"""Maximum allowed top-p value"""

# File upload constraints
MAX_FILE_SIZE_MB: Final[int] = 100
"""Maximum file upload size in MB"""

SUPPORTED_DOCUMENT_TYPES: Final[tuple] = (
    "application/pdf",
    "text/plain"
)
"""Supported document MIME types"""

SUPPORTED_FILE_EXTENSIONS: Final[tuple] = (
    "pdf",
    "txt"
)
"""Supported file extensions"""


def validate_configuration() -> bool:
    """
    Validate the application configuration.
    
    Returns:
        bool: True if configuration is valid, False otherwise
        
    Raises:
        ValueError: If critical configuration values are invalid
    """
    errors = []
    
    # Validate temperature
    if not (MIN_TEMPERATURE <= DEFAULT_TEMPERATURE <= MAX_TEMPERATURE):
        errors.append(
            f"DEFAULT_TEMPERATURE {DEFAULT_TEMPERATURE} must be between "
            f"{MIN_TEMPERATURE} and {MAX_TEMPERATURE}"
        )
    
    # Validate top-k
    if not (MIN_TOP_K <= DEFAULT_TOP_K <= MAX_TOP_K):
        errors.append(
            f"DEFAULT_TOP_K {DEFAULT_TOP_K} must be between "
            f"{MIN_TOP_K} and {MAX_TOP_K}"
        )
    
    # Validate top-p
    if not (MIN_TOP_P <= DEFAULT_TOP_P <= MAX_TOP_P):
        errors.append(
            f"DEFAULT_TOP_P {DEFAULT_TOP_P} must be between "
            f"{MIN_TOP_P} and {MAX_TOP_P}"
        )
    
    # Validate timeouts
    if HEALTH_CHECK_TIMEOUT <= 0:
        errors.append(f"HEALTH_CHECK_TIMEOUT must be positive")
    
    if MODELS_FETCH_TIMEOUT <= 0:
        errors.append(f"MODELS_FETCH_TIMEOUT must be positive")
    
    if MODEL_EXECUTION_TIMEOUT <= 0:
        errors.append(f"MODEL_EXECUTION_TIMEOUT must be positive")
    
    # Validate cache TTL
    if MODELS_CACHE_TTL < 0:
        errors.append(f"MODELS_CACHE_TTL must be non-negative")
    
    if errors:
        error_msg = "Configuration validation failed:\n" + "\n".join(errors)
        raise ValueError(error_msg)
    
    return True


# Validate configuration on import
try:
    validate_configuration()
except ValueError as e:
    import sys
    print(f"FATAL: {e}", file=sys.stderr)
    sys.exit(1)
