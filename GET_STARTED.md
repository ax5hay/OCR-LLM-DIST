# 🚀 GET STARTED IN 2 MINUTES

Welcome! Your OCR-LLM Distributed Chat is ready to use. Here's how to get started.

---

## Step 1: Setup (1 minute)

### macOS / Linux
```bash
bash setup.sh
```

### Windows
```bash
setup.bat
```

This will:
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Check Ollama availability
- ✅ Create .env configuration

---

## Step 2: Start Ollama (New Terminal)

```bash
ollama serve
```

You should see: `Listening on 127.0.0.1:11434`

---

## Step 3: Launch Application (Original Terminal)

```bash
streamlit run app.py
```

You should see:
```
You can now view your Streamlit app in your browser.
URL: http://localhost:8501
```

---

## 🎉 Done!

Open http://localhost:8501 and start chatting!

---

## 📚 Next Steps

### Learn More
- **Quick Setup**: [QUICKSTART.md](./QUICKSTART.md) - Detailed setup guide
- **Complete Guide**: [README.md](./README.md) - Full documentation
- **API Reference**: [API.md](./API.md) - Code examples
- **Navigation**: [DOCUMENTATION_INDEX.md](./DOCUMENTATION_INDEX.md) - Find anything

### Common Tasks

**Select a different model:**
1. In sidebar, click "Select Model" dropdown
2. Choose from available models
3. Or use: `ollama pull llama2:7b` to install new ones

**Upload a document:**
1. In sidebar, click "Upload a PDF or TXT file"
2. Select your file
3. Ask questions about the document!

**Change parameters:**
1. In sidebar, adjust Temperature, Top-P, Top-K
2. See [README.md](./README.md#-configuration) for what they mean

### Troubleshooting

**"Cannot connect to Ollama"?**
- Make sure `ollama serve` is running in another terminal
- Check: `curl http://localhost:11434/api/version`

**"Model not found"?**
- Download a model: `ollama pull deepseek-r1:1.5b`
- List models: `ollama list`

**Issues?**
- Check [QUICKSTART.md](./QUICKSTART.md#troubleshooting)
- See [README.md](./README.md#-troubleshooting)
- Report on [GitHub Issues](https://github.com/ax5hay/OCR-LLM-DIST/issues)

---

## 🐳 Alternative: Docker Setup

```bash
# One-command deployment
docker-compose up -d

# Access at http://localhost:8501
```

---

## 📖 Documentation Map

- **[README.md](./README.md)** ⭐ Start here for full docs
- **[QUICKSTART.md](./QUICKSTART.md)** - Detailed setup & troubleshooting
- **[API.md](./API.md)** - For developers
- **[DOCUMENTATION_INDEX.md](./DOCUMENTATION_INDEX.md)** - Find anything

---

## ✨ Features

✅ Chat with local AI models
✅ Upload and analyze documents (PDF, TXT)
✅ Real-time streaming responses
✅ Adjust model parameters
✅ Persistent chat history
✅ Document preview

---

**Enjoy! 🎉**

Got questions? Check [DOCUMENTATION_INDEX.md](./DOCUMENTATION_INDEX.md) for navigation help.

**Happy coding! 🚀**
