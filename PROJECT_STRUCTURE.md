# Project Structure Documentation

## Directory Layout

```
OCR-LLM-DIST/
│
├── 📄 Core Application Files
│   ├── app.py                      # Main Streamlit application
│   ├── config.py                   # Configuration management
│   ├── run_app.py                  # Alternative launcher with ngrok support
│   └── setup.py                    # Python package setup
│
├── 📦 Dependencies & Configuration
│   ├── requirements.txt            # Production dependencies
│   ├── requirements-dev.txt        # Development dependencies
│   ├── .env.example                # Environment variables template
│   ├── .gitignore                  # Git ignore rules
│   ├── .pre-commit-config.yaml     # Pre-commit hooks configuration
│   ├── .bandit                     # Security scanning configuration
│   ├── pytest.ini                  # Testing configuration
│   └── .streamlit/
│       └── config.toml             # Streamlit configuration
│
├── 🐳 Containerization
│   ├── Dockerfile                  # Docker image definition
│   └── docker-compose.yml          # Multi-container orchestration
│
├── 📚 Documentation
│   ├── README.md                   # Main documentation (comprehensive)
│   ├── QUICKSTART.md               # Quick start guide
│   ├── CONTRIBUTING.md             # Contribution guidelines
│   ├── API.md                      # API reference documentation
│   ├── LICENSE                     # MIT License
│   └── PROJECT_STRUCTURE.md        # This file
│
├── 🔧 Business Logic (services/)
│   ├── __init__.py                 # Package initialization
│   ├── model_service.py            # LLM inference & streaming
│   │   ├── validate_model_parameters()  # Parameter validation
│   │   └── run_model()                  # Main inference function
│   │
│   └── ollama_service.py           # Ollama API interactions
│       ├── check_api_health()      # Health check
│       ├── get_available_models()  # Model discovery
│       └── validate_model_name()   # Model validation
│
├── 🛠️ Utilities (utils/)
│   ├── __init__.py                 # Package initialization
│   ├── file_utils.py               # Document processing
│   │   ├── extract_text_from_doc() # Main extraction function
│   │   ├── validate_file()         # File validation
│   │   ├── _process_pdf()          # PDF processing
│   │   └── _process_text_file()    # Text file processing
│   │
│   └── logging_config.py           # Logging setup
│       └── setup_logger()          # Logger configuration
│
├── 🧪 Tests (tests/) - [To be created]
│   ├── __init__.py
│   ├── test_ollama_service.py
│   ├── test_model_service.py
│   ├── test_file_utils.py
│   └── test_integration.py
│
├── 📊 Cache & Temp (auto-generated)
│   └── __pycache__/
│
└── 📄 Build & Distribution
    ├── build/                      # Build output (auto-generated)
    ├── dist/                       # Distribution packages (auto-generated)
    └── *.egg-info/                 # Egg info (auto-generated)
```

---

## Module Descriptions

### Core Application (`app.py`)
**Main Streamlit UI orchestration**

Key Functions:
- `main()` - Application entry point
- `setup_sidebar()` - Model selection and parameter controls
- `process_document_upload()` - Document handling UI
- `setup_chat_interface()` - Chat message display and input

Dependencies:
- Streamlit for UI
- `services.model_service` for inference
- `services.ollama_service` for API integration
- `utils.file_utils` for document processing
- `utils.logging_config` for logging

---

### Configuration (`config.py`)
**Centralized configuration management**

Key Features:
- Environment variable support
- Type-safe constants using `Final`
- Comprehensive validation
- Parameter constraints definition
- Automatic validation on import

Configuration Hierarchy:
1. Environment variables (highest priority)
2. `.env` file
3. Hardcoded defaults (lowest priority)

---

### Services Module (`services/`)
**Business logic and external API integration**

#### `ollama_service.py`
Handles all Ollama API interactions:
- Health checking
- Model discovery with caching
- Automatic retries with exponential backoff
- Robust error handling

#### `model_service.py`
Manages LLM inference:
- Streaming response handling
- Parameter validation and clamping
- Token-by-token processing
- Performance metric collection

---

### Utils Module (`utils/`)
**Reusable utility functions**

#### `file_utils.py`
Document processing:
- PDF text extraction with PyMuPDF
- Text file processing with encoding detection
- File validation
- Error recovery with fallback encodings

#### `logging_config.py`
Logging infrastructure:
- Colored console output
- Structured log format
- Optional file logging with rotation
- Full diagnostic information

---

## Data Flow

### Chat Interaction Flow
```
User Input
    ↓
[app.py] → Validates input
    ↓
[model_service.py] → Validates parameters
    ↓
[ollama_service.py] → Checks API health & gets models
    ↓
[Ollama API] → Generates response (streaming)
    ↓
[model_service.py] → Streams chunks to UI
    ↓
[app.py] → Displays in real-time to user
```

### Document Upload Flow
```
User Uploads File
    ↓
[app.py] → Receives file object
    ↓
[file_utils.py] → Validates file format
    ↓
[file_utils.py] → Extracts text (PDF or TXT)
    ↓
[app.py] → Displays preview
    ↓
[app.py] → Includes in prompts with document context
```

---

## Key Design Patterns

### 1. Generator Pattern (Streaming)
```python
def run_model(...) -> Generator[str, None, None]:
    # Yields chunks as they arrive
    for chunk in response:
        yield chunk
```

### 2. Validation Pattern
```python
def validate_model_parameters(...) -> tuple:
    # Validates and clamps parameters
    return (clamped_temp, clamped_k, clamped_p)
```

### 3. Error Resilience
```python
# Retry strategy with exponential backoff
retry_strategy = Retry(
    total=3,
    backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504]
)
```

### 4. Logging & Monitoring
```python
# Structured logging with performance metrics
logger.success(f"Response: {duration:.2f}s, {tokens} tokens")
```

---

## Dependencies

### Production (`requirements.txt`)
- **streamlit** (1.22.0+) - Web UI framework
- **PyMuPDF** (1.23.7+) - PDF text extraction
- **loguru** (0.7.2+) - Structured logging
- **requests** (2.31.0+) - HTTP client with retries

### Development (`requirements-dev.txt`)
- **black** - Code formatting
- **pylint** - Linting
- **mypy** - Type checking
- **pytest** - Testing framework
- **pre-commit** - Git hooks
- **sphinx** - Documentation generation

---

## Configuration Priorities

### Example: DEFAULT_TEMPERATURE
```python
# Priority 1: Environment variable (highest)
export DEFAULT_TEMPERATURE=0.5

# Priority 2: .env file
# DEFAULT_TEMPERATURE=0.5

# Priority 3: config.py default (lowest)
DEFAULT_TEMPERATURE: Final[float] = 0.7
```

---

## Extension Points

### Adding New Services
1. Create `services/new_service.py`
2. Define functions with type hints
3. Import in `app.py`
4. Add comprehensive error handling
5. Add logging at appropriate levels

### Adding New Utilities
1. Create `utils/new_util.py`
2. Use logging for diagnostics
3. Add validation functions
4. Document with docstrings
5. Add to `utils/__init__.py`

### Adding Tests
1. Create `tests/test_module.py`
2. Use pytest framework
3. Mock external services
4. Aim for >80% coverage
5. Run: `pytest --cov`

---

## File Size Considerations

```
Estimated File Sizes (Production):
├── app.py                  ~10 KB
├── config.py               ~8 KB
├── services/
│   ├── model_service.py   ~7 KB
│   └── ollama_service.py  ~6 KB
├── utils/
│   ├── file_utils.py      ~6 KB
│   └── logging_config.py  ~2 KB
├── Dockerfile             ~1 KB
└── README.md              ~50 KB
```

---

## Performance Characteristics

### Response Times
- Health check: <100ms
- Model list fetch (cached): <10ms
- Model inference: Depends on model (1-30s typically)
- File extraction: Depends on file size

### Memory Usage
- Base application: ~50MB
- Ollama models: 1-7GB each
- Recommended total: 4GB minimum, 8GB+ recommended

---

## Security Considerations

### File Upload
- Validates file extension
- Validates MIME type
- Size limit: 100MB
- Encoding detection for safety

### API Communication
- SSL/TLS ready
- CORS configurable
- Rate limiting ready
- Input validation on all fields

### Configuration
- Secrets via environment variables
- `.env` in `.gitignore`
- Credentials never logged
- Audit logging available

---

## Future Extension Architecture

### Planned Additions
```
OCR-LLM-DIST/
├── services/
│   ├── database_service.py    # Database operations
│   ├── auth_service.py        # Authentication/Authorization
│   ├── cache_service.py       # Advanced caching
│   └── queue_service.py       # Async job processing
├── models/
│   ├── chat_history.py        # Data models
│   └── user.py
├── database/
│   ├── migrations/
│   └── schema.py
├── tests/
│   └── [test files]
└── api/
    └── endpoints.py           # REST API endpoints
```

---

## Version History

### v1.0.0 (Current)
- ✅ Core chat functionality
- ✅ Document upload & OCR
- ✅ Multi-model support
- ✅ Production-ready configuration
- ✅ Comprehensive logging
- ✅ Docker support

### v1.1.0 (Planned)
- [ ] REST API endpoints
- [ ] User authentication
- [ ] Chat history database
- [ ] Advanced caching strategies

### v2.0.0 (Planned)
- [ ] Model fine-tuning
- [ ] RAG integration
- [ ] Image OCR
- [ ] Batch processing

---

For more information, see:
- [README.md](./README.md) - Complete documentation
- [QUICKSTART.md](./QUICKSTART.md) - Quick start guide
- [API.md](./API.md) - API reference
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Contribution guidelines
