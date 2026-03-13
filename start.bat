@echo off
echo Markdown to PDF Converter
echo ========================

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt -q

REM Start server
echo Starting server...
echo Open http://localhost:8000 in your browser
echo Press Ctrl+C to stop
echo.
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
