@echo off
REM Setup script for OCR-LLM Distributed Chat application (Windows)
REM Automates the setup process for development and production

echo.
echo 🚀 OCR-LLM Distributed Chat - Setup Script (Windows)
echo ====================================================
echo.

REM Check Python version
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo ✓ Python is installed

REM Create virtual environment
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

REM Activate virtual environment
echo 📦 Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated

REM Upgrade pip
echo 🔄 Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1
echo ✓ Pip upgraded

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt >nul 2>&1
echo ✓ Dependencies installed

REM Ask if user wants to install dev dependencies
set /p install_dev="Install development dependencies? (y/n): "
if /i "%install_dev%"=="y" (
    echo 📚 Installing development dependencies...
    pip install -r requirements-dev.txt >nul 2>&1
    echo ✓ Development dependencies installed
    
    echo 🔧 Setting up pre-commit hooks...
    pre-commit install >nul 2>&1
    echo ✓ Pre-commit hooks installed
)

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo 📝 Creating .env file...
    copy .env.example .env >nul
    echo ✓ .env file created (using defaults)
)

REM Check if Ollama is running
echo.
echo 🔍 Checking for Ollama service...
curl -s http://localhost:11434/api/version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Ollama is running
) else (
    echo ⚠️  Ollama is not running
    echo    Start Ollama with: ollama serve
)

echo.
echo ====================================================
echo ✅ Setup complete!
echo.
echo Next steps:
echo   1. Start Ollama (if not already running):
echo      ollama serve
echo.
echo   2. Run the application:
echo      streamlit run app.py
echo.
echo   3. Open in browser:
echo      http://localhost:8501
echo.
echo For more information, see QUICKSTART.md
echo.
pause
