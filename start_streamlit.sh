#!/bin/bash

# OCR-LLM Streamlit Startup Script
# Starts backend and Streamlit UI

set -e

echo "🚀 OCR-LLM Streamlit - Starting services..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

print_status() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Cleanup
cleanup() {
    print_status "Shutting down..."
    pkill -f "python3 api_server.py" 2>/dev/null || true
    pkill -f "streamlit run" 2>/dev/null || true
    sleep 1
    print_success "Services stopped"
}

trap cleanup EXIT

echo "📋 Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required"
    exit 1
fi
print_success "Python found"

# Check pip
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is required"
    exit 1
fi
print_success "pip3 found"

echo ""
print_status "Installing Streamlit (if needed)..."
pip3 install -q streamlit requests 2>/dev/null || pip3 install streamlit requests

echo ""
print_status "Starting backend..."
cd "$SCRIPT_DIR"
python3 api_server.py > /tmp/ocr-llm-backend.log 2>&1 &
BACKEND_PID=$!
print_success "Backend PID: $BACKEND_PID"

sleep 3

# Test backend
if curl -s http://127.0.0.1:8000/api/health?backend=lmstudio > /dev/null 2>&1; then
    print_success "Backend is healthy"
else
    print_status "Backend not responding yet (this is OK)"
fi

echo ""
print_status "Starting Streamlit UI..."
streamlit run streamlit_app.py

