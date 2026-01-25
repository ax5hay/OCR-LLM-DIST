#!/bin/bash

# OCR-LLM SaaS - Complete Startup Script
# Starts both backend and frontend services

set -e

echo "🚀 OCR-LLM SaaS - Starting services..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Function to print status
print_status() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check if required commands exist
check_command() {
    if ! command -v $1 &> /dev/null; then
        print_error "$1 is not installed"
        return 1
    fi
    return 0
}

# Kill processes on exit
cleanup() {
    print_warning "Shutting down services..."
    pkill -f "python3 api_server.py" 2>/dev/null || true
    pkill -f "next dev" 2>/dev/null || true
    pkill -f "npm run dev" 2>/dev/null || true
    sleep 1
    print_success "Services stopped"
}

trap cleanup EXIT

echo "📋 Checking prerequisites..."

# Check Python
if check_command python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_success "Python $PYTHON_VERSION found"
else
    print_error "Python 3 is required"
    exit 1
fi

# Check Node
if check_command node; then
    NODE_VERSION=$(node --version)
    print_success "Node $NODE_VERSION found"
else
    print_error "Node.js is required"
    exit 1
fi

# Check npm
if check_command npm; then
    NPM_VERSION=$(npm --version)
    print_success "npm $NPM_VERSION found"
else
    print_error "npm is required"
    exit 1
fi

echo ""
print_status "Starting backend service..."

# Start backend
cd "$SCRIPT_DIR"
python3 api_server.py > /tmp/ocr-llm-backend.log 2>&1 &
BACKEND_PID=$!

print_success "Backend PID: $BACKEND_PID"
print_status "Waiting for backend to start..."
sleep 3

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    print_error "Backend failed to start"
    cat /tmp/ocr-llm-backend.log
    exit 1
fi

# Test backend health
if curl -s http://127.0.0.1:8000/api/health?backend=lmstudio > /dev/null 2>&1; then
    print_success "Backend is healthy"
else
    print_warning "Backend not responding yet, this is OK"
fi

echo ""
print_status "Starting frontend service..."

# Start frontend
cd "$SCRIPT_DIR/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    print_status "Installing dependencies..."
    npm install --legacy-peer-deps
fi

npm run dev > /tmp/ocr-llm-frontend.log 2>&1 &
FRONTEND_PID=$!

print_success "Frontend PID: $FRONTEND_PID"
print_status "Waiting for frontend to start..."
sleep 5

# Check if frontend is running
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    print_error "Frontend failed to start"
    cat /tmp/ocr-llm-frontend.log
    exit 1
fi

# Find the actual port (might not be 3000 if busy)
FRONTEND_PORT=3000
for port in 3000 3001 3002 3003; do
    if curl -s http://localhost:$port > /dev/null 2>&1; then
        FRONTEND_PORT=$port
        break
    fi
done

echo ""
echo "════════════════════════════════════════════════════════"
echo ""
print_success "All services started successfully!"
echo ""
echo -e "${GREEN}📍 Service URLs:${NC}"
echo "  • Frontend:  ${BLUE}http://localhost:$FRONTEND_PORT${NC}"
echo "  • Backend:   ${BLUE}http://127.0.0.1:8000${NC}"
echo "  • Logs:      ${BLUE}/tmp/ocr-llm-*.log${NC}"
echo ""
echo -e "${YELLOW}⌚ Opening frontend in browser...${NC}"
echo ""

# Try to open in browser (macOS)
if command -v open &> /dev/null; then
    sleep 2
    open "http://localhost:$FRONTEND_PORT" 2>/dev/null || true
fi

echo "════════════════════════════════════════════════════════"
echo ""
print_status "Press Ctrl+C to stop all services"
echo ""

# Keep the script running
wait

