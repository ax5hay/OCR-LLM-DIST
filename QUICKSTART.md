# Getting Started Guide

## Quick Installation & Launch (5 minutes)

### Prerequisites
- Python 3.8+ 
- **Either** Ollama or LMStudio installed and running

### Step 1: Clone Repository
```bash
git clone https://github.com/ax5hay/OCR-LLM-DIST.git
cd OCR-LLM-DIST
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Start Your LLM Backend

**Option A: Ollama (Recommended for simplicity)**
```bash
# In a new terminal
ollama serve
```

**Option B: LMStudio**
1. Download from https://lmstudio.ai/
2. Launch the application
3. Download a model from the hub (auto-starts local API server)
4. Verify: `curl http://127.0.0.1:1234/v1/models`

### Step 5: Launch Application
```bash
# Original terminal
streamlit run app.py

# Optional: specify backend
export ACTIVE_LLM_BACKEND=lmstudio  # or "ollama"
streamlit run app.py
```

Open http://localhost:8501 in your browser! 🎉

---

## Detailed Setup for Different Scenarios

### macOS Setup
```bash
# Install Ollama using Homebrew
brew install ollama

# Start Ollama in background
ollama serve &

# Rest of setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Ubuntu/Linux Setup
```bash
# Download and install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama
ollama serve &

# Rest of setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Windows Setup (with WSL2 recommended)
```bash
# Using Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# In separate PowerShell window
ollama serve

# Back to first window
streamlit run app.py
```

### Docker Setup
```bash
# Build and run with Docker Compose (all-in-one)
docker-compose up -d

# Wait for services to start (30-45 seconds)
# Access app at http://localhost:8501
```

---

## Model Selection

### Pre-installed Models
Ollama comes with several models you can use:

**Lightweight (Recommended for laptops):**
- `deepseek-r1:1.5b` - ~1.5GB, fast, decent quality
- `phi:2.7b` - ~1.6GB, creative writing
- `neural-chat:7b` - ~4GB, conversational

**Balanced:**
- `llama2:7b` - ~3.8GB, general purpose
- `mistral:7b` - ~4.1GB, creative and technical

**High Quality (Needs 16GB+ RAM):**
- `neural-chat:13b` - ~7.4GB
- `llama2:13b` - ~7.3GB

### Downloading Models
```bash
# Pull a model
ollama pull deepseek-r1:1.5b
ollama pull llama2:7b

# List all downloaded models
ollama list

# Remove a model
ollama rm deepseek-r1:1.5b
```

---

## Development Setup

### Install Development Tools
```bash
pip install -r requirements-dev.txt
```

### Setup Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install

# Run hooks on all files
pre-commit run --all-files
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=services,utils --cov-report=html

# Run specific test file
pytest tests/test_model_service.py -v
```

### Code Quality
```bash
# Format code
black .

# Lint
pylint services/ utils/

# Type check
mypy services/ utils/
```

---

## Troubleshooting

### "Cannot connect to Ollama API"
```bash
# Check if Ollama is running
curl http://localhost:11434/api/version

# If not, start it
ollama serve

# Check firewall
# Port 11434 must be accessible
```

### "Model not found" Error
```bash
# List available models
ollama list

# Download the model
ollama pull deepseek-r1:1.5b

# Or select a different model in the app
```

### Out of Memory Errors
```bash
# Use smaller model
ollama pull phi:2.7b

# Or increase system RAM/enable GPU acceleration
```

### Port Already in Use
```bash
# Find process using port 8501
lsof -i :8501  # macOS/Linux
netstat -ano | findstr :8501  # Windows

# Kill the process or use different port
streamlit run app.py --server.port 8502
```

### Slow Performance
- Use a smaller model (1.5b-7b range)
- Ensure sufficient available RAM
- Enable GPU acceleration if available
- Reduce document size for uploads

---

## Configuration

### Using Environment Variables
```bash
# Create .env file
cp .env.example .env

# Edit .env
OLLAMA_API_BASE=http://localhost:11434
DEFAULT_MODEL=deepseek-r1:1.5b
DEFAULT_TEMPERATURE=0.7
```

### Common Configurations

**For Creativity (Creative Writing, Brainstorming):**
```env
DEFAULT_TEMPERATURE=0.9
DEFAULT_TOP_P=0.95
DEFAULT_TOP_K=50
```

**For Accuracy (Technical Questions, Facts):**
```env
DEFAULT_TEMPERATURE=0.3
DEFAULT_TOP_P=0.7
DEFAULT_TOP_K=30
```

**For Balance (Conversation):**
```env
DEFAULT_TEMPERATURE=0.7
DEFAULT_TOP_P=0.9
DEFAULT_TOP_K=40
```

---

## Next Steps

1. ✅ Explore the UI - Upload a document, try different parameters
2. 📚 Try different models - Compare responses quality/speed
3. 📖 Read full [README.md](./README.md)
4. 🤝 Contribute - See [CONTRIBUTING.md](./CONTRIBUTING.md)
5. 🐳 Deploy - Use Docker for production

---

## Need Help?

- **Issues**: [GitHub Issues](https://github.com/ax5hay/OCR-LLM-DIST/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ax5hay/OCR-LLM-DIST/discussions)
- **Ollama Help**: [Ollama Docs](https://ollama.ai/)
- **Streamlit Help**: [Streamlit Docs](https://docs.streamlit.io/)

Enjoy! 🚀
