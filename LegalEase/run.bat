@echo off
setlocal
cd /d "%~dp0"

echo ========================================================
echo   LegalEase: AI-Powered Legal Document Generator
echo ========================================================

:: 1. Create virtual environment if missing
if not exist "venv\Scripts\python.exe" (
    echo [1/4] Creating virtual environment...
    python -m venv venv
) else (
    echo [1/4] Virtual environment detected.
)

:: 2. Ensure .env exists in root directory
if not exist ".env" (
    if exist "docs\.env" (
        echo Moving .env from docs\ to project root...
        move /y "docs\.env" ".env" >nul
    ) else if exist ".env.example" (
        echo Creating .env from .env.example...
        copy /y ".env.example" ".env" >nul
        echo [WARNING] Please add your GEMINI_API_KEY inside the .env file!
    )
)

:: 3. Install/Verify dependencies using prebuilt wheels
echo [2/4] Verifying dependencies...
"venv\Scripts\python.exe" -m pip install --upgrade pip setuptools wheel --quiet
"venv\Scripts\python.exe" -m pip install --prefer-binary -r requirements.txt --quiet

:: 4. Start FastAPI Backend Server in a new window
echo [3/4] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "LegalEase - FastAPI Backend" cmd /k ""%~dp0venv\Scripts\python.exe" -m uvicorn legalEaseAPI.main:app --reload --host 127.0.0.1 --port 8000"

:: Wait 3 seconds for Backend to initialize
timeout /t 3 /nobreak >nul

:: 5. Start Streamlit Frontend UI in a new window
echo [4/4] Launching Streamlit Frontend on http://localhost:8501 ...
start "LegalEase - Streamlit UI" cmd /k ""%~dp0venv\Scripts\python.exe" -m streamlit run frontend/app.py"

echo ========================================================
echo   All services are running!
echo   - Backend API Docs : http://127.0.0.1:8000/docs
echo   - Streamlit Web UI : http://localhost:8501
echo ========================================================
pause