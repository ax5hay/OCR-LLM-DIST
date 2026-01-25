# 🧠 OCR-LLM Distributed Chat Platform

> A cutting-edge, production-grade distributed chat application that seamlessly integrates Optical Character Recognition (OCR) with Large Language Models (LLMs) to deliver intelligent document processing and conversational AI capabilities.

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-15.1-black.svg)](https://nextjs.org/)

**[⚡ Quick Start](#-quick-start) • [📚 Full Guide](QUICK_SETUP.md) • [🚀 Startup Options](STARTUP_OPTIONS.md) • [🔌 LMStudio Setup](LMSTUDIO_INTEGRATION.md)**

---

## ✨ Features

### 🚀 Core Capabilities
- **Intelligent Document Processing**: Extract text from PDF and TXT files with advanced OCR capabilities using PyMuPDF
- **Real-time Streaming Responses**: Experience low-latency AI responses with token-by-token streaming
- **Multi-Model Support**: Seamlessly switch between multiple LLMs with dynamic model loading
- **Advanced Parameter Control**: Fine-tune model behavior with temperature, top-p, and top-k parameters
- **Persistent Chat History**: Maintain conversation context throughout your session
- **Document Context Integration**: Automatically incorporate uploaded documents into your prompts for contextual queries

### 🏗️ Architecture Excellence
- **Modular Service Architecture**: Clean separation of concerns with dedicated service layers
- **Comprehensive Logging**: Production-grade logging with loguru for complete observability
- **Health Checks & Monitoring**: Automatic API health verification and status reporting
- **Error Resilience**: Graceful error handling with detailed diagnostic information
- **Performance Optimization**: Strategic caching to minimize latency and API calls
- **Type-Safe Codebase**: Comprehensive type hints for maintainability and IDE support

### � Multi-Backend LLM Support
- **Ollama Integration**: Native support for local Ollama inference engine
- **LMStudio Support**: Full integration with LMStudio's OpenAI-compatible API
- **Backend Switching**: Seamlessly switch between backends via UI or environment variables
- **Unified Interface**: Consistent API regardless of underlying backend
- **Dynamic Model Discovery**: Automatically discover available models from active backend

### �🔒 Production Features
- **Environment-Based Configuration**: Secure configuration management via environment variables
- **Docker Containerization**: Ready-to-deploy Docker and Docker Compose configurations
- **CORS & CSRF Protection**: Built-in security controls for web deployments
- **Rate Limiting Ready**: Foundation for implementing request throttling and quotas
- **Input Validation**: Comprehensive validation of all user inputs and API requests

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **At least one LLM Backend**:
  - **Ollama** ([Download](https://ollama.ai/)) - Recommended for beginners
  - **LMStudio** ([Download](https://lmstudio.ai/)) - Alternative option
- **Git** ([Download](https://git-scm.com/))

### System Requirements
- **RAM**: Minimum 4GB (8GB+ recommended for larger models)
- **Disk Space**: At least 5GB for base models
- **OS**: macOS, Linux, or Windows with WSL

---

## 🚀 Quick Start

### ⚡ 60-Second Launch (Recommended)

Choose your preferred interface:

**Full-Featured SaaS (Next.js):**
```bash
./start.sh
```
Opens beautiful Next.js UI with all features on http://localhost:3000

**Lightweight Option (Streamlit):**
```bash
./start_streamlit.sh
```
Opens simple Streamlit UI on http://localhost:8501

**See [Startup Options](STARTUP_OPTIONS.md) for complete details.**

---

### 📚 Complete Setup Guide

For detailed step-by-step instructions, see [QUICK_SETUP.md](QUICK_SETUP.md)

1. Clone repository
2. Install dependencies
3. Start LLM backend (LMStudio or Ollama)
4. Run startup script
5. Begin chatting!

---

### 🔌 LMStudio Setup

For detailed LMStudio configuration, see [LMSTUDIO_INTEGRATION.md](LMSTUDIO_INTEGRATION.md)

---

## 🐳 Docker Deployment

For Docker deployment instructions, see [QUICK_SETUP.md - Deployment Section](QUICK_SETUP.md)

---

## 🔌 Backend Comparison: Ollama vs LMStudio

| Feature | Ollama | LMStudio |
|---------|--------|----------|
| **Installation** | Command-line tool | GUI Application |
| **Ease of Use** | Moderate (terminal-based) | Easy (GUI-based) |
| **Model Management** | CLI commands | GUI interface |
| **API Format** | Custom format | OpenAI-compatible |
| **Supported Models** | Llama 2, Mistral, etc. | Extensive open-source models |
| **Memory Efficiency** | Optimized | Very efficient |
| **UI Features** | Minimal | Rich web UI |
| **Best For** | Server/CLI users | Desktop/GUI users |

### Switching Backends

**Via Environment Variable:**
```bash
# Use Ollama (default)
export ACTIVE_LLM_BACKEND=ollama
streamlit run app.py

# Use LMStudio
export ACTIVE_LLM_BACKEND=lmstudio
streamlit run app.py
```

**Via User Interface:**
1. Launch the application
2. Click on the 🔌 **LLM Backend** radio button in the sidebar
3. Select "ollama" or "lmstudio"
4. The UI will automatically detect and use the selected backend

### Health Checks

The application automatically verifies backend connectivity:
- **Ollama**: Checks `http://localhost:11434/api/tags`
- **LMStudio**: Checks `http://127.0.0.1:1234/v1/models`

If a backend is unavailable, the application will display an error with troubleshooting instructions.

---

## 📖 Usage Guide

### Basic Workflow

1. **Launch the Application**
   - Open http://localhost:8501 in your web browser
   - The application loads with model selection and document upload options

2. **Select a Model** (Sidebar)
   - Choose from available LLMs in the "Model Settings" section
   - Models are cached for 1 hour to minimize API calls

3. **Configure Parameters** (Sidebar)
   - **Temperature** (0.1-1.0): Controls randomness
     - Lower values (0.1-0.3): More deterministic, factual responses
     - Higher values (0.7-1.0): More creative, varied responses
   - **Top-P** (0.1-1.0): Nucleus sampling threshold
   - **Top-K** (1-100): Vocabulary size constraint

4. **Upload Documents** (Optional, Sidebar)
   - Supports PDF and TXT files
   - Extract text automatically
   - View document preview before querying

5. **Start Chatting**
   - Type your message in the chat interface
   - Press "Send 🚀" to submit
   - View streamed responses in real-time
   - Use "Clear Chat 🗑️" to reset conversation history

### Advanced Features

#### Document Context Integration
Upload a document, then ask questions about its content. The system automatically includes the document text in your prompt:
```
User: "Summarize the key points from the document"
System: Automatically adds document context to your prompt
```

#### Multi-Turn Conversations
- Full chat history is maintained throughout your session
- Each message is contextualized with previous exchanges
- Perfect for complex multi-step reasoning tasks

#### Streaming Responses
- Watch responses appear token-by-token
- Real-time feedback on model performance
- Detailed timing information in logs

---

## 🏗️ Project Architecture

```
OCR-LLM-DIST/
├── app.py                          # Main Streamlit application entry point
├── config.py                       # Configuration and constants
├── run_app.py                      # Alternative launcher with ngrok support
├── requirements.txt                # Python dependencies
├── requirements-dev.txt            # Development dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── Dockerfile                      # Docker image definition
├── docker-compose.yml              # Multi-container orchestration
├── README.md                       # This file
├── LICENSE                         # MIT License
├── CONTRIBUTING.md                 # Contribution guidelines
│
├── services/                       # Business logic services
│   ├── __init__.py
│   ├── model_service.py           # LLM inference and streaming
│   └── ollama_service.py          # Ollama API interactions
│
└── utils/                         # Utility functions
    ├── __init__.py
    ├── file_utils.py              # Document processing and OCR
    └── logging_config.py          # Logging setup and configuration
```

### Key Components

#### `app.py` - Main Application
- Streamlit UI orchestration
- Chat interface management
- User session handling
- Component lifecycle management

#### `services/model_service.py` - Model Inference
- Streaming request handling
- Token-by-token response generation
- Performance metrics collection
- Error handling and retries

#### `services/ollama_service.py` - API Integration
- Health checks and connectivity verification
- Dynamic model discovery and caching
- API error handling with fallbacks
- Robust error logging

#### `utils/file_utils.py` - Document Processing
- Multi-format document support (PDF, TXT)
- Intelligent text extraction
- Encoding detection and fallbacks
- Progress tracking and diagnostics

#### `utils/logging_config.py` - Observability
- Structured logging configuration
- Color-coded console output
- Full diagnostic information
- Performance metrics tracking

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Ollama API Configuration
OLLAMA_API_BASE=http://localhost:11434
OLLAMA_GENERATE_ENDPOINT=http://localhost:11434/api/generate
OLLAMA_MODELS_ENDPOINT=http://localhost:11434/api/tags
OLLAMA_VERSION_ENDPOINT=http://localhost:11434/api/version

# Model Configuration
DEFAULT_MODEL=deepseek-r1:1.5b
DEFAULT_TEMPERATURE=0.7
DEFAULT_TOP_K=40
DEFAULT_TOP_P=0.9

# Timeouts (in seconds)
HEALTH_CHECK_TIMEOUT=5
MODELS_FETCH_TIMEOUT=10
MODEL_EXECUTION_TIMEOUT=60

# Application Settings
MODELS_CACHE_TTL=3600
PAGE_TITLE=Chat with Local AI
PAGE_ICON=🧠

# Optional: Ngrok for Remote Access
NGROK_AUTH_TOKEN=your_ngrok_token_here
```

### Configuration Hierarchy
1. Environment variables (highest priority)
2. `.env` file
3. Hardcoded defaults in `config.py` (lowest priority)

---

## 📦 Installation Variants

### Minimal Installation
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Development Installation
```bash
# Install all dependencies including dev tools
pip install -r requirements.txt -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install

# Run tests
pytest
```

### Remote Access with Ngrok
```bash
# Install additional dependency
pip install pyngrok

# Run with ngrok tunnel
python run_app.py
# Enter your ngrok auth token when prompted
```

---

## 🧪 Development

### Setting Up Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt

# Setup pre-commit hooks for code quality
pre-commit install

# Run tests
pytest

# Run linting
black .
pylint services/ utils/
```

### Code Style

This project follows:
- **Black** for code formatting
- **Pylint** for code quality
- **Type hints** for type safety
- **Docstrings** for API documentation

### Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 🚨 Troubleshooting

### Connection Error: "Cannot connect to Ollama API"
**Problem**: Application shows connection error to Ollama
```
⚠️ Cannot connect to Ollama API. Please make sure Ollama is running on http://localhost:11434
```

**Solution**:
```bash
# Start Ollama in a separate terminal
ollama serve

# Verify connectivity
curl http://localhost:11434/api/version
```

### Model Not Found Error
**Problem**: Selected model not available
```
Error: Model 'model-name' not found
```

**Solution**:
```bash
# List available models
ollama list

# Download a model
ollama pull deepseek-r1:1.5b
ollama pull llama2
```

### Memory Errors with Large Models
**Problem**: Out of memory errors during model loading

**Solution**:
- Reduce model size: `ollama pull deepseek-r1:1.5b` (smaller)
- Increase system RAM or enable swap
- Use GPU acceleration if available

### Document Processing Failures
**Problem**: "Error extracting text from PDF"

**Solution**:
- Verify PDF is not corrupted: `file document.pdf`
- Try with a different PDF
- Check file permissions: `ls -la document.pdf`

### Streamlit Session State Issues
**Problem**: Chat history disappears or models don't update

**Solution**:
- Clear browser cache: `Ctrl+Shift+Delete` (or `Cmd+Shift+Delete` on Mac)
- Restart Streamlit: `Ctrl+C` and rerun `streamlit run app.py`
- Check browser console for JavaScript errors

---

## 📊 Performance Optimization

### Response Time Improvements
- **Model Caching**: Available models are cached for 1 hour (configurable)
- **Streaming**: Token-by-token streaming for perceived faster responses
- **Connection Pooling**: Reuses HTTP connections to Ollama API

### Scaling Considerations
- **Vertical Scaling**: Increase RAM/GPU for larger models
- **Horizontal Scaling**: Deploy multiple instances behind a load balancer
- **Model Quantization**: Use quantized model versions for better performance

### Monitoring
View performance metrics in the application logs:
```
✓ Response completed in 12.34s | Length: 1234 chars | 45 chunks | 3.6 tokens/sec
```

---

## 🔐 Security Considerations

### For Production Deployments
1. **API Authentication**: Implement authentication layer for Ollama API
2. **HTTPS**: Use TLS/SSL certificates for encrypted communication
3. **Rate Limiting**: Enable rate limiting to prevent abuse
4. **Input Validation**: All inputs are validated (see `services/`)
5. **CORS Configuration**: Properly configure CORS headers
6. **Secret Management**: Never commit `.env` files to version control

### Security Checklist
- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS in production
- [ ] Implement authentication/authorization
- [ ] Set up request rate limiting
- [ ] Configure firewall rules
- [ ] Enable audit logging
- [ ] Regular security updates

---

## 📈 Roadmap

### Upcoming Features
- [ ] **Multi-Model Comparison**: Run same query on multiple models
- [ ] **Conversation Export**: Save chats as PDF/Markdown
- [ ] **RAG Integration**: Enhanced context retrieval from documents
- [ ] **Image OCR**: Extract text from images
- [ ] **Model Fine-tuning**: Custom model adaptation
- [ ] **API REST Endpoint**: Programmatic access layer
- [ ] **Database Integration**: Persistent conversation storage
- [ ] **User Authentication**: Multi-user support with history
- [ ] **Advanced Analytics**: Usage metrics and insights
- [ ] **Batch Processing**: Queue-based job management

---

## 📞 Support & Community

### Getting Help
- **Issues**: [GitHub Issues](https://github.com/ax5hay/OCR-LLM-DIST/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ax5hay/OCR-LLM-DIST/discussions)
- **Documentation**: [Complete Docs](./docs/)

### Related Projects
- [Ollama](https://ollama.ai/) - Local LLM inference
- [Streamlit](https://streamlit.io/) - Python app framework
- [PyMuPDF](https://pymupdf.readthedocs.io/) - PDF processing

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Akshay

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🙏 Acknowledgments

- **Ollama Team** for the incredible local LLM inference engine
- **Streamlit Community** for the amazing app framework
- **PyMuPDF Contributors** for robust PDF processing
- **All Contributors** who have helped improve this project

---

## 📊 Project Statistics

- **Lines of Code**: 700+
- **Core Modules**: 7
- **API Integrations**: 1 (Ollama)
- **Supported File Formats**: 2 (PDF, TXT)
- **Python Version**: 3.8+
- **License**: MIT

---

**Built with ❤️ by the OCR-LLM team**

⭐ If you find this project helpful, please consider giving it a star on GitHub!
