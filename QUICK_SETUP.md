# 🚀 Complete Setup Guide - OCR-LLM

> For quick startup options, see [Startup Options](STARTUP_OPTIONS.md)
> For LMStudio setup, see [LMStudio Integration](LMSTUDIO_INTEGRATION.md)

## ⚡ 60-Second Quick Start

### Option A: Full SaaS (Next.js Frontend)
```bash
chmod +x start.sh
./start.sh
```
**Opens automatically at http://localhost:3000**

### Option B: Lightweight UI (Streamlit)
```bash
chmod +x start_streamlit.sh
./start_streamlit.sh
```
**Opens automatically at http://localhost:8501**

### Option C: Manual (Development)
```bash
# Terminal 1: Backend
python3 api_server.py

# Terminal 2: Frontend (Next.js)
cd frontend && npm run dev

# OR Frontend (Streamlit)
streamlit run streamlit_app.py
```

---

## 📋 Prerequisites

- **Python 3.9+** - For backend
- **Node.js 18+** - For Next.js frontend (skip if using Streamlit)
- **LMStudio or Ollama** - Running locally with models loaded
- **macOS/Linux** - (WSL on Windows)

### Check Prerequisites
```bash
python3 --version     # Should show 3.9+
node --version        # Should show 18+ (skip if Streamlit)
npm --version         # Should show 8+ (skip if Streamlit)
```

---

## 🎯 Which Interface?

### **Next.js SaaS** (Recommended)
- ✅ Full-featured web application
- ✅ Beautiful dark theme UI
- ✅ Real-time markdown rendering
- ✅ Stop generation button
- ✅ Scrollable during streaming
- ✅ Production-ready

**Use: `./start.sh`**

### **Streamlit UI** (Simple)
- ✅ Lightweight & quick to deploy
- ✅ No build step required
- ✅ Works in browser/notebooks
- ✅ Good for prototyping
- ❌ Less polished UI

**Use: `./start_streamlit.sh`**

---

## 🛠️ Detailed Setup

### Step 1: Verify LMStudio
1. Open LMStudio app
2. Go to "Local Server" tab
3. Ensure at least one model is loaded
4. Server should be running on `http://127.0.0.1:1234`

### Step 2: Check Backend Connection
```bash
# Test backend can reach LMStudio
curl http://127.0.0.1:1234/v1/models
```

Should return: `{"object":"list","data":[...]}`

### Step 3: Start Services
```bash
./start.sh  # For Next.js
# OR
./start_streamlit.sh  # For Streamlit
```

### Step 4: Open in Browser
- **Next.js**: http://localhost:3000
- **Streamlit**: http://localhost:8501

---

## 📝 Usage

### Chat
1. Select a model from sidebar
2. Type message in chat input
3. Hit Enter or click Send
4. AI responds with streaming text

### Upload Document
1. Click "Attach" button
2. Select PDF or TXT file
3. Content becomes context for future messages

### Stop Generation
- Click the red "Stop" button during streaming
- Generation will be interrupted

### Adjust Parameters
- **Temperature** (0.0-2.0): Creativity vs focus
- **Top-K** (0-100): Token sampling variety
- **Top-P** (0.0-1.0): Nucleus sampling

---

## 🔧 Configuration

### Backend Settings
File: `api_server.py`

```python
# Change host/port
host="0.0.0.0"      # Listen on all interfaces
port=8000           # API port
```

### Frontend Settings (Next.js)
File: `.env.local` (create if needed)

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

### Streamlit Settings
File: `.streamlit/config.toml` (create if needed)

```toml
[server]
port = 8501
headless = true
```

---

## 🐛 Troubleshooting

### "Failed to fetch" Error
```bash
# Issue: Frontend can't reach backend
# Solution: Use 127.0.0.1 instead of localhost
# Already configured! Just ensure:
lsof -i :8000  # Backend is on 8000
curl http://127.0.0.1:8000/api/health  # Returns JSON
```

### Models Not Loading
```bash
# Issue: No models show in UI
# Check:
curl http://127.0.0.1:1234/v1/models

# If empty: Load model in LMStudio app
# If error: LMStudio not running on 1234
```

### Port Already in Use
```bash
# Find what's using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>

# Or change port in api_server.py
```

### Build Errors (Next.js)
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
npm run build
npm run dev
```

### Streamlit Not Installing
```bash
pip3 install --upgrade pip
pip3 install streamlit requests
streamlit run streamlit_app.py
```

### LMStudio Issues
For detailed LMStudio setup and troubleshooting, see [LMSTUDIO_INTEGRATION.md](LMSTUDIO_INTEGRATION.md)

---

## 📊 API Endpoints

Access directly or use UI:

```bash
# Health
GET http://127.0.0.1:8000/api/health?backend=lmstudio

# Models
GET http://127.0.0.1:8000/api/models?backend=lmstudio

# Chat (streaming)
POST http://127.0.0.1:8000/api/chat
  ?message=Hello
  &model=MODEL_NAME
  &backend=lmstudio

# Upload
POST http://127.0.0.1:8000/api/upload
  (multipart form with file)

# Config
GET http://127.0.0.1:8000/api/config
```

---

## 🎓 Examples

### Python Client
```python
import requests

response = requests.get(
    "http://127.0.0.1:8000/api/models?backend=lmstudio"
)
models = response.json()["models"]
print(models)
```

### JavaScript Client
```javascript
const response = await fetch(
  "http://127.0.0.1:8000/api/health?backend=lmstudio"
);
const data = await response.json();
console.log(data);
```

### cURL
```bash
curl -X POST "http://127.0.0.1:8000/api/chat" \
  -d "message=Hello&model=mistral&backend=lmstudio"
```

---

## 📦 Project Structure
```
OCR-LLM-DIST/
├── start.sh                 # Start all services (Next.js)
├── start_streamlit.sh       # Start with Streamlit
├── api_server.py            # FastAPI backend
├── streamlit_app.py         # Streamlit UI
├── config.py                # Configuration
├── frontend/                # Next.js app
│   ├── src/
│   │   ├── app/
│   │   └── components/
│   └── package.json
├── services/                # LLM services
│   ├── model_service.py
│   ├── lmstudio_service.py
│   └── ollama_service.py
└── utils/                   # Utilities
    ├── file_utils.py
    └── logging_config.py
```

---

## 🚀 Deployment

### Local (Development)
```bash
./start.sh  # Auto-detects best port
```

### Docker
Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "api_server.py"]
```

### Production (Next.js)
```bash
cd frontend
npm run build
npm run start  # Production server
```

### Production (Streamlit)
```bash
streamlit run streamlit_app.py \
  --server.port=8501 \
  --server.headless=true
```

---

## 📞 Support

- **Port Issues**: Try `./start.sh` (auto-detects)
- **Backend Down**: Check LMStudio is running
- **Models Missing**: Load in LMStudio app
- **Frontend Errors**: Check `/tmp/ocr-llm-*.log`

---

## ✅ Verification Checklist

- [ ] LMStudio running on 1234
- [ ] Models loaded in LMStudio
- [ ] Backend started on 8000
- [ ] Frontend started on 3000/8501
- [ ] Can access http://localhost:3000 (or :8501)
- [ ] Backend health returns "healthy"
- [ ] Models list shows available models
- [ ] Can type and send messages
- [ ] Can upload PDF/TXT files

---

## 🎉 You're Ready!

Enjoy using OCR-LLM! Start with `./start.sh` and let it handle everything else.

