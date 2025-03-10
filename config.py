"""
Configuration settings for the Local Chat application.
"""

# Ollama API configuration
OLLAMA_API_BASE = "http://localhost:11434"
OLLAMA_GENERATE_ENDPOINT = f"{OLLAMA_API_BASE}/api/generate"
OLLAMA_MODELS_ENDPOINT = f"{OLLAMA_API_BASE}/api/tags"
OLLAMA_VERSION_ENDPOINT = f"{OLLAMA_API_BASE}/api/version"

# Default model settings
DEFAULT_MODEL = "deepseek-r1:1.5b"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_K = 40
DEFAULT_TOP_P = 0.9

# Request timeouts (seconds)
HEALTH_CHECK_TIMEOUT = 5
MODELS_FETCH_TIMEOUT = 10
MODEL_EXECUTION_TIMEOUT = 60

# Cache settings
MODELS_CACHE_TTL = 3600  # 1 hour

# Application settings
PAGE_TITLE = "Chat with Local AI"
PAGE_ICON = "🧠"