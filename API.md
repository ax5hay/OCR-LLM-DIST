# API Reference

## Services Module

### `ollama_service.py`

#### `check_api_health() → bool`
Check if the Ollama API is available and healthy.

**Returns:**
- `True` if API is healthy
- `False` if API is unreachable or unhealthy

**Example:**
```python
from services.ollama_service import check_api_health

if check_api_health():
    print("API is ready!")
else:
    print("API is down")
```

---

#### `get_available_models() → List[str]`
Get a list of available models from the Ollama API.

**Returns:**
- List of model names as strings
- Returns `[DEFAULT_MODEL]` if no models found or error occurs

**Example:**
```python
from services.ollama_service import get_available_models

models = get_available_models()
print(f"Available models: {models}")
# Output: Available models: ['deepseek-r1:1.5b', 'llama2:7b']
```

---

#### `validate_model_name(model_name: str) → bool`
Validate that a model name is available.

**Parameters:**
- `model_name` (str): Name of the model to validate

**Returns:**
- `True` if model exists
- `False` if model doesn't exist or error occurs

**Example:**
```python
from services.ollama_service import validate_model_name

if validate_model_name("deepseek-r1:1.5b"):
    print("Model is available")
```

---

### `lmstudio_service.py`

#### `check_api_health() → bool`
Check if the LMStudio API is available and healthy.

**Returns:**
- `True` if API is healthy
- `False` if API is unreachable or unhealthy

**Endpoint Checked:** `GET http://127.0.0.1:1234/v1/models`

**Example:**
```python
from services.lmstudio_service import check_api_health

if check_api_health():
    print("LMStudio API is ready!")
else:
    print("LMStudio API is down or unreachable at http://127.0.0.1:1234")
```

---

#### `get_available_models() → List[str]`
Get a list of available models from the LMStudio API.

**Returns:**
- List of model IDs as strings
- Returns `[]` if no models found or error occurs

**Endpoint:** `GET http://127.0.0.1:1234/v1/models`

**Response Format:**
```json
{
  "data": [
    {"id": "neural-chat-7b-v3-1", "object": "model"},
    {"id": "mistral-7b-instruct-v0.1", "object": "model"}
  ]
}
```

**Example:**
```python
from services.lmstudio_service import get_available_models

models = get_available_models()
print(f"Available models: {models}")
# Output: Available models: ['neural-chat-7b-v3-1', 'mistral-7b-instruct-v0.1']
```

---

#### `validate_model_name(model_name: str) → bool`
Validate that a model name is available in LMStudio.

**Parameters:**
- `model_name` (str): Name of the model to validate

**Returns:**
- `True` if model exists
- `False` if model doesn't exist or error occurs

**Example:**
```python
from services.lmstudio_service import validate_model_name

if validate_model_name("neural-chat-7b-v3-1"):
    print("Model is available in LMStudio")
```

---

### `model_service.py` - Multi-Backend Support

#### `run_model(prompt, model, temperature, top_k, top_p, backend=None) → Generator[str]`
Run a model inference with the specified parameters on either Ollama or LMStudio backend.

**Parameters:**
- `prompt` (str): The input prompt for the model **[Required]**
- `model` (str): The model name to use (default: `DEFAULT_MODEL`)
- `temperature` (float): Generation temperature, 0.1-1.0 (default: 0.7)
- `top_k` (int): Top-K sampling parameter, 1-100 (default: 40, Ollama only)
- `top_p` (float): Top-P nucleus sampling parameter, 0.0-1.0 (default: 0.9)
- `backend` (str, optional): "ollama" or "lmstudio". Uses `ACTIVE_LLM_BACKEND` if None

**Yields:**
- str: Generated text chunks or error messages

**Raises:**
- `ValueError`: If prompt is empty or backend is invalid

**Backend-Specific Behavior:**
- **Ollama**: Uses `/api/generate` endpoint with top_k parameter
- **LMStudio**: Uses OpenAI-compatible `/v1/chat/completions` endpoint

**Example - Ollama:**
```python
from services.model_service import run_model

prompt = "What is machine learning?"
for chunk in run_model(prompt, model="deepseek-r1:1.5b", backend="ollama"):
    print(chunk, end="", flush=True)
```

**Example - LMStudio:**
```python
from services.model_service import run_model

prompt = "What is machine learning?"
for chunk in run_model(prompt, model="neural-chat-7b-v3-1", backend="lmstudio"):
    print(chunk, end="", flush=True)
```

**Example - Auto-Select Backend:**
```python
from services.model_service import run_model
# Uses ACTIVE_LLM_BACKEND from config

for chunk in run_model("Hello world"):
    print(chunk, end="", flush=True)
```

---

#### `validate_model_parameters(temperature, top_k, top_p) → tuple`
Validate and clamp model parameters to acceptable ranges.

**Parameters:**
- `temperature` (float): Generation temperature
- `top_k` (int): Top-K sampling parameter
- `top_p` (float): Top-P nucleus sampling parameter

**Returns:**
- tuple: Clamped (temperature, top_k, top_p) parameters

**Example:**
```python
from services.model_service import validate_model_parameters

temp, k, p = validate_model_parameters(
    temperature=1.5,  # Will be clamped to 1.0
    top_k=150,        # Will be clamped to 100
    top_p=0.5
)
print(f"Validated: {temp}, {k}, {p}")
# Output: Validated: 1.0, 100, 0.5
```

---

## Utils Module

### `file_utils.py`

#### `extract_text_from_doc(uploaded_file) → str`
Extract text from uploaded document (PDF or text file).

**Parameters:**
- `uploaded_file`: Streamlit uploaded file object with:
  - `.name` (str): Filename
  - `.type` (str): MIME type
  - `.read()` method: Returns file bytes

**Returns:**
- str: Extracted text or error message

**Supported Formats:**
- PDF files (application/pdf)
- Text files (text/plain)

**Example:**
```python
from utils.file_utils import extract_text_from_doc

text = extract_text_from_doc(uploaded_file)
if text.startswith("Error:"):
    print(f"Failed: {text}")
else:
    print(f"Extracted {len(text)} characters")
```

---

#### `validate_file(uploaded_file) → tuple[bool, Optional[str]]`
Validate an uploaded file.

**Parameters:**
- `uploaded_file`: Streamlit uploaded file object

**Returns:**
- tuple: (is_valid, error_message)
  - `is_valid` (bool): True if file is valid
  - `error_message` (Optional[str]): None if valid, error string otherwise

**Example:**
```python
from utils.file_utils import validate_file

is_valid, error = validate_file(uploaded_file)
if is_valid:
    text = extract_text_from_doc(uploaded_file)
else:
    print(f"Invalid file: {error}")
```

---

### `logging_config.py`

#### `setup_logger(level=None, log_file=None)`
Configure the logger with appropriate format and settings.

**Parameters:**
- `level` (Optional[str]): Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL). Defaults to `LOG_LEVEL` from config.
- `log_file` (Optional[str]): Optional file path for logging output

**Returns:**
- loguru.Logger: Configured logger instance

**Example:**
```python
from utils.logging_config import setup_logger

logger = setup_logger(level="DEBUG")
logger.info("Application started")
logger.success("Operation completed")
logger.error("An error occurred")
```

---

## Configuration Module

### Constants

#### Ollama Configuration
- `OLLAMA_API_BASE` (str): Base URL for Ollama API
- `OLLAMA_GENERATE_ENDPOINT` (str): Text generation endpoint
- `OLLAMA_MODELS_ENDPOINT` (str): Models list endpoint
- `OLLAMA_VERSION_ENDPOINT` (str): Version/health endpoint

#### LMStudio Configuration
- `LMSTUDIO_API_BASE` (str): Base URL for LMStudio API (default: http://127.0.0.1:1234)
- `LMSTUDIO_MODELS_ENDPOINT` (str): Models list endpoint (/v1/models)
- `LMSTUDIO_CHAT_COMPLETIONS_ENDPOINT` (str): Chat completions endpoint (/v1/chat/completions)
- `LMSTUDIO_COMPLETIONS_ENDPOINT` (str): Text completions endpoint (/v1/completions)

#### Backend Selection
- `ACTIVE_LLM_BACKEND` (str): Select active backend ("ollama" or "lmstudio", default: "ollama")

#### Model Settings
- `DEFAULT_MODEL` (str): Default LLM model
- `DEFAULT_TEMPERATURE` (float): Default generation temperature
- `DEFAULT_TOP_K` (int): Default top-K parameter
- `DEFAULT_TOP_P` (float): Default top-P parameter

#### Timeouts (seconds)
- `HEALTH_CHECK_TIMEOUT` (int): API health check timeout
- `MODELS_FETCH_TIMEOUT` (int): Model list fetch timeout
- `MODEL_EXECUTION_TIMEOUT` (int): Model inference timeout

#### Constraints
- `MIN_TEMPERATURE`, `MAX_TEMPERATURE` (float): 0.1 - 1.0
- `MIN_TOP_K`, `MAX_TOP_K` (int): 1 - 100
- `MIN_TOP_P`, `MAX_TOP_P` (float): 0.0 - 1.0
- `MAX_FILE_SIZE_MB` (int): 100 MB
- `SUPPORTED_FILE_EXTENSIONS` (tuple): ("pdf", "txt")

#### Application Settings
- `PAGE_TITLE` (str): Browser page title
- `PAGE_ICON` (str): Browser page icon/emoji
- `LOG_LEVEL` (str): Logging level
- `MODELS_CACHE_TTL` (int): Model cache time-to-live (seconds)

---

### Functions

#### `validate_configuration() → bool`
Validate the application configuration.

**Returns:**
- `True` if configuration is valid

**Raises:**
- `ValueError`: If any configuration value is invalid

**Example:**
```python
from config import validate_configuration

try:
    validate_configuration()
    print("Configuration is valid")
except ValueError as e:
    print(f"Configuration error: {e}")
```

---

## Environment Variables

Configure the application behavior using environment variables in a `.env` file or system variables.

### Backend Configuration
```bash
# Select LLM backend (default: ollama)
ACTIVE_LLM_BACKEND=lmstudio  # or ollama

# LMStudio API endpoints
LMSTUDIO_API_BASE=http://127.0.0.1:1234
LMSTUDIO_MODELS_ENDPOINT=http://127.0.0.1:1234/v1/models
LMSTUDIO_CHAT_COMPLETIONS_ENDPOINT=http://127.0.0.1:1234/v1/chat/completions
LMSTUDIO_COMPLETIONS_ENDPOINT=http://127.0.0.1:1234/v1/completions

# Ollama API endpoints (default values shown)
OLLAMA_API_BASE=http://localhost:11434
OLLAMA_GENERATE_ENDPOINT=http://localhost:11434/api/generate
OLLAMA_MODELS_ENDPOINT=http://localhost:11434/api/tags
OLLAMA_VERSION_ENDPOINT=http://localhost:11434/api/version
```

### Model Configuration
```bash
# Default model to use
DEFAULT_MODEL=neural-chat

# Default generation parameters
DEFAULT_TEMPERATURE=0.7
DEFAULT_TOP_K=40
DEFAULT_TOP_P=0.9
```

### Timeout Configuration
```bash
# API request timeouts (in seconds)
HEALTH_CHECK_TIMEOUT=5
MODELS_FETCH_TIMEOUT=10
MODEL_EXECUTION_TIMEOUT=300  # 5 minutes for long generations
```

### Application Configuration
```bash
# Logging level
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Model cache TTL (time-to-live in seconds)
MODELS_CACHE_TTL=3600  # 1 hour
```

### Example .env File
```bash
# Backend selection
ACTIVE_LLM_BACKEND=lmstudio

# LMStudio Configuration
LMSTUDIO_API_BASE=http://127.0.0.1:1234

# Model Settings
DEFAULT_MODEL=neural-chat-7b-v3-1
DEFAULT_TEMPERATURE=0.7

# Timeouts
MODEL_EXECUTION_TIMEOUT=600

# Logging
LOG_LEVEL=INFO
```

---

## Usage Examples

### Complete Chat Flow
```python
import streamlit as st
from services.ollama_service import check_api_health, get_available_models
from services.model_service import run_model
from utils.file_utils import extract_text_from_doc

# Check API health
if not check_api_health():
    st.error("Ollama API is down")
    st.stop()

# Get available models
models = get_available_models()
selected_model = st.selectbox("Select Model", models)

# File upload (optional)
uploaded_file = st.file_uploader("Upload document", type=["pdf", "txt"])
document_text = ""
if uploaded_file:
    document_text = extract_text_from_doc(uploaded_file)

# Chat
prompt = st.text_input("Your question")
if st.button("Send"):
    if document_text:
        prompt = f"Document:\n{document_text}\n\nQuestion: {prompt}"
    
    for chunk in run_model(prompt, model=selected_model):
        st.write(chunk, end="")
```

---

## Error Handling Best Practices

```python
from services.model_service import run_model
from utils.logging_config import setup_logger

logger = setup_logger()

try:
    for response in run_model("Hello"):
        if response.startswith("Error:"):
            logger.error(f"API Error: {response}")
            break
        print(response, end="", flush=True)
except Exception as e:
    logger.exception(f"Unexpected error: {e}")
```

---

## Rate Limiting Example

```python
import time
from functools import wraps
from utils.logging_config import setup_logger

logger = setup_logger()

def rate_limit(min_interval=1.0):
    """Decorator to rate limit function calls"""
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            
            last_called[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(min_interval=0.5)
def call_model(prompt):
    from services.model_service import run_model
    return run_model(prompt)
```

---

## Performance Monitoring Example

```python
import time
from utils.logging_config import setup_logger
from services.model_service import run_model

logger = setup_logger()

def monitor_performance(prompt, model):
    start = time.time()
    chunk_count = 0
    
    for chunk in run_model(prompt, model=model):
        chunk_count += 1
    
    elapsed = time.time() - start
    logger.info(f"Performance: {elapsed:.2f}s, {chunk_count} chunks")
```

---

For more information, see [README.md](./README.md) and [CONTRIBUTING.md](./CONTRIBUTING.md).
