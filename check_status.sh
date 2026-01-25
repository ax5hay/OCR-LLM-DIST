#!/bin/bash
# OCR-LLM System Startup Script

echo "🚀 OCR-LLM SAAS - System Status Check"
echo "════════════════════════════════════════════════════════════"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "Checking Services..."
echo ""

# Check Frontend
echo -n "Frontend (localhost:3000)... "
if curl -s http://localhost:3000 > /dev/null 2>&1; then
  echo -e "${GREEN}✅ RUNNING${NC}"
else
  echo -e "${RED}❌ DOWN${NC}"
  echo "  Start with: cd /Users/akshay/OCR-LLM-DIST/frontend && npm run dev"
fi

# Check Backend
echo -n "Backend (localhost:8000)... "
if curl -s http://localhost:8000/api/health | grep -q "healthy"; then
  echo -e "${GREEN}✅ HEALTHY${NC}"
else
  echo -e "${RED}❌ DOWN${NC}"
  echo "  Start with: cd /Users/akshay/OCR-LLM-DIST && python3 api_server.py"
fi

# Check Models
echo -n "LMStudio Models... "
MODELS=$(curl -s http://localhost:8000/api/models | grep -o '"count": [0-9]*' | grep -o '[0-9]*')
if [ ! -z "$MODELS" ]; then
  echo -e "${GREEN}✅ $MODELS MODELS${NC}"
else
  echo -e "${RED}❌ NO MODELS${NC}"
  echo "  Ensure LMStudio is running on port 1234"
fi

echo ""
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📖 Documentation:"
echo "   • GETTING_STARTED.md - User guide (START HERE!)"
echo "   • SYSTEM_STATUS.md   - Technical details"
echo ""
echo "🌐 Access Application:"
echo "   http://localhost:3000"
echo ""
echo "════════════════════════════════════════════════════════════"
