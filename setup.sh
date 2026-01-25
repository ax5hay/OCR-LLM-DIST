#!/bin/bash
# Setup script for OCR-LLM Distributed Chat application
# Automates the setup process for development and production

set -e  # Exit on error

echo "🚀 OCR-LLM Distributed Chat - Setup Script"
echo "=========================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

required_version="3.8"
if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "✗ Python 3.8+ is required (found: $python_version)"
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo "🔄 Upgrading pip, setuptools, and wheel..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo "✓ Pip upgraded"

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Dependencies installed"

# Ask if user wants to install dev dependencies
read -p "Install development dependencies? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📚 Installing development dependencies..."
    pip install -r requirements-dev.txt > /dev/null 2>&1
    echo "✓ Development dependencies installed"
    
    # Setup pre-commit hooks
    echo "🔧 Setting up pre-commit hooks..."
    pre-commit install > /dev/null 2>&1
    echo "✓ Pre-commit hooks installed"
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created (using defaults)"
fi

# Check if Ollama is running
echo ""
echo "🔍 Checking for Ollama service..."
if curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
    echo "✓ Ollama is running"
    
    # Get available models
    echo "📋 Available models:"
    curl -s http://localhost:11434/api/tags | python3 -m json.tool | grep '"name"' || true
else
    echo "⚠️  Ollama is not running"
    echo "   Start Ollama with: ollama serve"
fi

echo ""
echo "=========================================="
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Start Ollama (if not already running):"
echo "     ollama serve"
echo ""
echo "  2. Run the application:"
echo "     streamlit run app.py"
echo ""
echo "  3. Open in browser:"
echo "     http://localhost:8501"
echo ""
echo "For more information, see QUICKSTART.md"
