# 🚀 Startup Options - Quick Comparison

> See [README.md](README.md) for overview  
> See [QUICK_SETUP.md](QUICK_SETUP.md) for detailed setup  
> See [LMSTUDIO_INTEGRATION.md](LMSTUDIO_INTEGRATION.md) for LMStudio setup

## Quick Summary

Three ways to run OCR-LLM:

| Option | Command | UI | Speed | Features |
|--------|---------|----|----|----------|
| **SaaS** | `./start.sh` | Next.js | 3 sec | Full-featured ✨ |
| **Streamlit** | `./start_streamlit.sh` | Streamlit | 2 sec | Simple & clean |
| **Manual** | See below | Your choice | 1 sec | Developer mode |

---

## Option 1: Full SaaS (Recommended) 🎯

**Best for**: Production, full features, beautiful UI

```bash
./start.sh
```

**What happens:**
- ✅ Checks prerequisites (Python, Node, npm)
- ✅ Starts FastAPI backend on `http://127.0.0.1:8000`
- ✅ Installs frontend dependencies (if needed)
- ✅ Starts Next.js dev server on `http://localhost:3000`
- ✅ Automatically opens browser

**Features included:**
- 🎨 Beautiful dark theme with gradient UI
- 📊 Real-time markdown rendering
- ⏹️ Stop generation button
- 📜 Scroll chat while LLM is typing
- 🎛️ Advanced parameter controls
- 📁 Document upload support
- 🚀 Production-ready frontend

**Time to start:** ~3-5 seconds

---

## Option 2: Streamlit UI ⚡

**Best for**: Quick demos, simple interface, no build overhead

```bash
./start_streamlit.sh
```

**What happens:**
- ✅ Checks Python & pip
- ✅ Installs streamlit & requests (if needed)
- ✅ Starts FastAPI backend on `http://127.0.0.1:8000`
- ✅ Starts Streamlit server on `http://localhost:8501`
- ✅ Opens browser automatically

**Features included:**
- 💬 Clean chat interface
- 🎚️ Parameter sliders
- 📤 File upload
- 🔄 Live model selection
- ✨ Auto-refresh on model change

**Time to start:** ~2-3 seconds

---

## Option 3: Manual Startup 🔧

**Best for**: Development, debugging, multiple windows

### Backend Only
```bash
python3 api_server.py
```
Available at: `http://127.0.0.1:8000`

### Frontend (Next.js)
```bash
cd frontend
npm install              # Only needed once
npm run dev
```
Available at: `http://localhost:3000`

### Frontend (Streamlit)
```bash
pip install streamlit requests
streamlit run streamlit_app.py
```
Available at: `http://localhost:8501`

---

## File Descriptions

### `start.sh`
- **Size:** 4.0 KB
- **Language:** Bash
- **Purpose:** Complete SaaS startup
- **Features:**
  - Prerequisite checking
  - Process management
  - Auto-open browser
  - Colored output
  - Graceful shutdown

### `start_streamlit.sh`
- **Size:** 1.6 KB
- **Language:** Bash
- **Purpose:** Streamlit + Backend startup
- **Features:**
  - Minimal dependencies
  - Fast startup
  - Auto-open browser

### `streamlit_app.py`
- **Size:** 5.2 KB
- **Language:** Python
- **Purpose:** Streamlit user interface
- **Features:**
  - Sidebar configuration
  - Chat history
  - Document upload
  - Parameter adjustment
  - Backend communication

### `QUICK_SETUP.md`
- **Purpose:** Comprehensive quick start guide
- **Contents:**
  - 60-second quick start
  - Prerequisites checklist
  - Detailed setup steps
  - Configuration options
  - Troubleshooting guide
  - API documentation
  - Deployment options

### `QUICK_START.md` (Updated)
- **Purpose:** Original quick start (now includes new options)

---

## Architecture

```
OCR-LLM-DIST
│
├─ start.sh ──────────┬─→ Backend (FastAPI) ──→ LMStudio/Ollama
│                     │
│                     └─→ Frontend (Next.js) ──→ Browser
│
├─ start_streamlit.sh ┬─→ Backend (FastAPI) ──→ LMStudio/Ollama
│                     │
│                     └─→ Streamlit UI ────────→ Browser
│
└─ Manual
   ├─→ python3 api_server.py
   ├─→ npm run dev (or streamlit run streamlit_app.py)
   └─→ Open browser
```

---

## Feature Comparison

### Next.js SaaS
```
✅ Beautiful gradient UI
✅ Markdown rendering
✅ Stop generation button
✅ Smart auto-scroll
✅ Parameter controls
✅ File upload
✅ Production-ready
✅ Dark theme
✅ Responsive design
❌ Requires Node.js
❌ Requires build step
```

### Streamlit UI
```
✅ Simple setup (Python only)
✅ No build required
✅ Live parameter adjustment
✅ Chat history
✅ File upload
✅ Responsive
❌ Less polished UI
❌ Basic styling
❌ No markdown rendering
```

---

## Troubleshooting

### "Port already in use"
```bash
# For Next.js: Auto-detects and switches to 3001, 3002, 3003
# For Streamlit: Manually change port in start_streamlit.sh

# Find what's using port:
lsof -i :8000

# Kill it:
kill -9 <PID>
```

### "Backend won't start"
```bash
# Check if LMStudio is running
curl http://127.0.0.1:1234/v1/models

# Check Python installation
python3 --version  # Should be 3.9+

# Install dependencies if needed
pip install -r requirements.txt
```

### "Frontend won't load"
```bash
# For Next.js:
cd frontend && npm install --legacy-peer-deps

# For Streamlit:
pip install streamlit requests
```

### "Models not showing"
1. Open LMStudio app
2. Go to "Local Server" tab
3. Load a model
4. Verify port 1234 is active
5. Restart the script

---

## Development Tips

### Watch Backend Logs
```bash
tail -f /tmp/ocr-llm-backend.log
```

### Watch Frontend Logs
```bash
tail -f /tmp/ocr-llm-frontend.log
```

### Test Backend Directly
```bash
curl http://127.0.0.1:8000/api/health?backend=lmstudio
curl http://127.0.0.1:8000/api/models?backend=lmstudio
```

### Rebuild Frontend
```bash
cd frontend
npm run build
npm run dev
```

---

## Production Deployment

### Docker with Next.js
```dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY frontend .
RUN npm install && npm run build

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["npm", "start"]
```

### Docker with Streamlit
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements_streamlit.txt
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

### Environment Variables
```bash
export BACKEND_HOST=0.0.0.0
export BACKEND_PORT=8000
export LLM_BACKEND=lmstudio
export LMSTUDIO_URL=http://127.0.0.1:1234
```

---

## Next Steps

1. **Choose your interface:**
   - Want full features? → `./start.sh`
   - Want something quick? → `./start_streamlit.sh`
   - Developing? → Manual startup

2. **Run the startup script**

3. **Open the URL in your browser**

4. **Select a model and start chatting!**

---

## Additional Resources

- [Full Quick Start Guide](QUICK_SETUP.md)
- [API Documentation](API.md)
- [Installation Guide](INSTALLATION_GUIDE.md)
- [LMStudio Integration](LMSTUDIO_INTEGRATION.md)

---

**That's it! You're ready to use OCR-LLM. Pick your preferred interface and go! 🚀**

