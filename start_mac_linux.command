#!/bin/bash
cd "$(dirname "$0")"

echo "============================================"
echo "  CipherMind - Setup and Launch"
echo "============================================"

# 1. Check for .env file
if [ ! -f ".env" ]; then
    echo "No .env file found."
    echo "Creating one from .env.example ..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Open the new .env file and add your"
    echo "HF_API_TOKEN and GROQ_API_KEY_1 before continuing."
    echo ""
    read -p "Press Enter once you've added your keys..."
fi

# 2. Create virtual environment if missing
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# 3. Install dependencies
echo "Installing dependencies (first run only, may take a few minutes)..."
pip install -q -r requirements.txt

# 4. Open the browser after a short delay, then start the server
( sleep 2 && (open http://127.0.0.1:8000 2>/dev/null || xdg-open http://127.0.0.1:8000 2>/dev/null) ) &

echo "Starting CipherMind server..."
python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
