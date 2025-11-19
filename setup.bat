@echo off
REM Setup script for Letterboxd Movie Matcher (Windows)
REM This creates a virtual environment and installs dependencies

echo 🎬 Setting up Letterboxd Movie Matcher...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.7+ first.
    pause
    exit /b 1
)

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment.
    pause
    exit /b 1
)

echo ✓ Virtual environment created
echo.

REM Activate and install
echo 📥 Installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ✅ Setup complete!
echo.
echo To run the app:
echo   1. Activate the virtual environment:
echo      venv\Scripts\activate
echo.
echo   2. Start the server:
echo      cd backend
echo      python app.py
echo.
echo   3. Open http://localhost:5000 in your browser
pause

