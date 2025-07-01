#!/bin/bash

# Ali 2025 Campaign Bot - Local Production Hosting Script

echo "🚀 Setting up Ali 2025 Campaign Bot for local hosting..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if serve is installed globally
if ! command_exists serve; then
    echo -e "${YELLOW}Installing 'serve' globally...${NC}"
    npm install -g serve
fi

# Kill any existing processes on the ports we want to use
echo -e "${BLUE}Cleaning up existing processes...${NC}"
lsof -ti:8080 | xargs kill -9 2>/dev/null || true
lsof -ti:8081 | xargs kill -9 2>/dev/null || true

# Function to cleanup background processes
cleanup() {
    echo -e "\n${YELLOW}Shutting down services...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

echo -e "${GREEN}🎉 Starting Ali 2025 Campaign Bot in production mode...${NC}"
echo -e "${BLUE}Backend API: http://localhost:8081${NC}"
echo -e "${BLUE}Frontend: http://localhost:8080${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop both services${NC}"
echo ""

# Start backend on port 8081
cd backend
echo -e "${BLUE}Starting backend server...${NC}"
source venv/bin/activate

# Update the backend to use port 8081
export FLASK_ENV=production
export FLASK_DEBUG=False

# Start backend using gunicorn for production
gunicorn --bind 0.0.0.0:8081 --workers 2 --timeout 60 src.app:app &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend on port 8080
cd ../frontend
echo -e "${BLUE}Starting frontend server...${NC}"

# Serve the built frontend
serve -s build -l 8080 &
FRONTEND_PID=$!

echo -e "${GREEN}✅ Both services are now running!${NC}"
echo -e "${BLUE}🌐 Open your browser and go to: http://localhost:8080${NC}"
echo ""
echo -e "${YELLOW}The bot is ready to assist with Mussab Ali's 2025 campaign!${NC}"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
