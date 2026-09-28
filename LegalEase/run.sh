#!/usr/bin/env bash
set -e

echo "========================================================"
echo "  LegalEase: AI-Powered Legal Document Generator"
echo "========================================================"

# 1. Create virtual environment if missing
if [ ! -d "venv" ]; then
    echo "[1/4] Creating virtual environment..."
    python3 -m venv venv || python -m venv venv
fi

# 2. Resolve Python executable path (Windows Git Bash vs Unix)
if [ -f "venv/Scripts/python.exe" ]; then
    PY_EXEC="venv/Scripts/python.exe"
else
    PY_EXEC="venv/bin/python"
fi

# 3. Install dependencies with prebuilt binary preference
echo "[2/4] Installing dependencies..."
"$PY_EXEC" -m pip install --upgrade pip setuptools wheel --quiet
"$PY_EXEC" -m pip install --prefer-binary -r requirements.txt --quiet

# 4. Launch FastAPI Backend in background
echo "[3/4] Starting FastAPI Backend on http://127.0.0.1:8000 ..."
"$PY_EXEC" -m uvicorn legalEaseAPI.main:app --reload --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

# Ensure backend process is terminated when script exits
trap "echo 'Stopping FastAPI Backend...'; kill $BACKEND_PID 2>/dev/null || true" EXIT

sleep 2

# 5. Launch Streamlit Frontend
echo "[4/4] Starting Streamlit Frontend on http://localhost:8501 ..."
"$PY_EXEC" -m streamlit run frontend/app.py