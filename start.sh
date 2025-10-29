#!/bin/bash

# 🚀 Quick Start Script for TravelMate
# This script sets up and runs both frontend and backend servers

echo "🌍 TravelMate - Starting Development Servers"
echo "=============================================="

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "⚠️  MongoDB is not running!"
    echo "Starting MongoDB..."
    brew services start mongodb-community 2>/dev/null || sudo systemctl start mongod 2>/dev/null
    sleep 2
fi

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "📦 Creating Python virtual environment..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
else
    echo "✅ Virtual environment found"
fi

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  No .env file found!"
    echo "📝 Creating .env from template..."
    cp backend/.env.example backend/.env
    echo ""
    echo "⚠️  IMPORTANT: Edit backend/.env and add your API keys:"
    echo "   - GEMINI_API_KEY (get from https://makersuite.google.com/app/apikey)"
    echo "   - JWT_SECRET (generate a random string)"
    echo ""
    read -p "Press Enter to continue after updating .env..."
fi

# Kill any existing processes on ports
echo "🧹 Cleaning up existing processes..."
lsof -ti:5002 | xargs kill -9 2>/dev/null
lsof -ti:8000 | xargs kill -9 2>/dev/null
sleep 1

# Start backend
echo "🔧 Starting Backend Server (Port 5002)..."
cd backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend
echo "🎨 Starting Frontend Server (Port 8000)..."
cd frontend
python3 -m http.server 8000 &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Servers Started Successfully!"
echo "================================"
echo "🎨 Frontend: http://localhost:8000"
echo "🔧 Backend:  http://127.0.0.1:5002"
echo "💚 Health:   http://127.0.0.1:5002/health"
echo ""
echo "📝 Backend PID: $BACKEND_PID"
echo "📝 Frontend PID: $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for user to stop
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo ''; echo '👋 Servers stopped'; exit" INT
wait
