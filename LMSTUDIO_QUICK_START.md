# 🔌 LMStudio Integration - Quick Reference

## Start Here

### For LMStudio Users

```bash
# 1. Download LMStudio
# Visit: https://lmstudio.ai/
# Install and launch the application

# 2. Download a model
# Use the model hub in LMStudio to download a model

# 3. Verify API is running
curl http://127.0.0.1:1234/v1/models

# 4. Set backend and start app
export ACTIVE_LLM_BACKEND=lmstudio
streamlit run app.py

# 5. Open browser
# http://localhost:8501
```

### For Ollama Users (No Changes)

```bash
# Everything works exactly as before
ollama serve
streamlit run app.py
```

---

## Backend Selection

### Option 1: Via Environment Variable (Startup)
```bash
# Before starting app
export ACTIVE_LLM_BACKEND=lmstudio  # or "ollama"
streamlit run app.py
```

### Option 2: Via UI (Runtime)
1. Open app at http://localhost:8501
2. Look for "🔌 LLM Backend" radio button in sidebar
3. Click "lmstudio" or "ollama"
4. Models list updates automatically ✅

### Option 3: Via .env File
```bash
# Create or edit .env file
echo "ACTIVE_LLM_BACKEND=lmstudio" >> .env

# Start app (auto-loads from .env)
streamlit run app.py
```

---

## API Endpoints

### LMStudio (Default: http://127.0.0.1:1234)
```bash
# List models
curl http://127.0.0.1:1234/v1/models

# Chat with model
curl http://127.0.0.1:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "neural-chat-7b-v3-1",
    "messages": [{"role": "user", "content": "Hi"}],
    "stream": true
  }'
```

### Ollama (Default: http://localhost:11434)
```bash
# List models
curl http://localhost:11434/api/tags

# Generate text
curl http://localhost:11434/api/generate \
  -d '{"model": "deepseek-r1:1.5b", "prompt": "Hi"}'
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Cannot connect to LMStudio" | Verify: `curl http://127.0.0.1:1234/v1/models` |
| "No models showing" | Download models in LMStudio app |
| Backend selector not appearing | Clear cache: `rm -rf .streamlit/` & restart |
| Models loading slowly | Models are cached for 1 hour (normal) |
| Wrong backend active | Check env var: `echo $ACTIVE_LLM_BACKEND` |

---

## Configuration

### Basic Setup
```bash
# Use defaults (works out of box)
streamlit run app.py
```

### Custom LMStudio Port
```bash
export LMSTUDIO_API_BASE=http://192.168.1.100:1234
streamlit run app.py
```

### All Environment Variables
```bash
# Backend selection
export ACTIVE_LLM_BACKEND=lmstudio

# LMStudio endpoints
export LMSTUDIO_API_BASE=http://127.0.0.1:1234
export LMSTUDIO_MODELS_ENDPOINT=http://127.0.0.1:1234/v1/models
export LMSTUDIO_CHAT_COMPLETIONS_ENDPOINT=http://127.0.0.1:1234/v1/chat/completions

# Model defaults
export DEFAULT_MODEL=neural-chat-7b-v3-1
export DEFAULT_TEMPERATURE=0.7
export DEFAULT_TOP_P=0.9

# Timeouts
export MODEL_EXECUTION_TIMEOUT=600
export HEALTH_CHECK_TIMEOUT=5

# Logging
export LOG_LEVEL=INFO

# Then start
streamlit run app.py
```

---

## File Reference

| File | Purpose | Status |
|------|---------|--------|
| `services/lmstudio_service.py` | LMStudio integration | ✅ New |
| `services/model_service.py` | Multi-backend inference | ✅ Enhanced |
| `app.py` | Streamlit UI | ✅ Enhanced |
| `config.py` | Configuration | ✅ Enhanced |
| `README.md` | Documentation | ✅ Enhanced |
| `QUICKSTART.md` | Setup guide | ✅ Enhanced |
| `API.md` | API reference | ✅ Enhanced |

---

## Code Examples

### Python: Use LMStudio
```python
from services.model_service import run_model

# Stream response from LMStudio
for chunk in run_model(
    "Hello, how are you?",
    model="neural-chat-7b-v3-1",
    backend="lmstudio"
):
    print(chunk, end="", flush=True)
```

### Python: Auto-Select Backend
```python
from services.model_service import run_model
from config import ACTIVE_LLM_BACKEND

# Uses ACTIVE_LLM_BACKEND setting
for chunk in run_model("Hello world"):
    print(chunk, end="", flush=True)
```

### Check Backend Health
```python
from services.lmstudio_service import check_api_health

if check_api_health():
    print("✅ LMStudio is ready!")
else:
    print("❌ LMStudio is unreachable")
```

### Get Available Models
```python
from services.lmstudio_service import get_available_models

models = get_available_models()
for model in models:
    print(f"  - {model}")
```

---

## Performance Tips

### For Better Streaming Speed
1. Use SSD storage for models
2. Allocate 8GB+ RAM
3. Use high-end GPU if available
4. Close other applications
5. Use 4-bit or 8-bit quantized models

### For LMStudio Specifically
1. Download models directly in LMStudio app
2. Start API from LMStudio UI (more reliable)
3. Use localhost (127.0.0.1) for local access
4. Monitor LMStudio window to see GPU usage

### For Ollama Specifically
1. Run `ollama serve` in separate terminal
2. Pre-load model with `ollama pull model-name`
3. Use native Ollama command for consistency

---

## Common Model Names

### LMStudio Models
- `neural-chat-7b-v3-1`
- `mistral-7b-instruct-v0.1`
- `llama-2-7b-chat`
- `dolphin-2.1-mistral-7b`

### Ollama Models
- `deepseek-r1:1.5b`
- `llama2:7b`
- `mistral:7b`
- `neural-chat:7b`

---

## Support

### Documentation
- Full docs: `README.md`
- Setup guide: `QUICKSTART.md`
- API reference: `API.md`
- Implementation details: `LMSTUDIO_INTEGRATION.md`

### Debugging
1. Check logs for `[Ollama]` or `[LMStudio]` tags
2. Verify API endpoints respond to curl
3. Check model names match backend
4. Ensure no port conflicts

### Environment
- Python 3.8+
- LMStudio from https://lmstudio.ai/
- OR Ollama from https://ollama.ai/
- Both support macOS, Linux, Windows (WSL)

---

**Last Updated**: 2024  
**Status**: ✅ Production Ready  
**Backends**: Ollama + LMStudio  
**Next Steps**: Open app at http://localhost:8501
