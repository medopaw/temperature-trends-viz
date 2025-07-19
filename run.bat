@echo off
setlocal enabledelayedexpansion

REM Temperature Trends Viz - Startup Script for Windows
REM This script simplifies running the application with uv

echo 🌡️  Temperature Trends Viz Startup Script
echo ==========================================

REM Check if uv is installed
uv --version >nul 2>&1
if errorlevel 1 (
    echo ❌ uv is not installed. Please install it first:
    echo    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    echo    Or visit: https://docs.astral.sh/uv/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('uv --version') do set UV_VERSION=%%i
echo ✅ uv found: !UV_VERSION!

REM Check if we're in the right directory
if not exist "weather_gui.py" (
    echo ❌ weather_gui.py not found. Please run this script from the project root directory.
    pause
    exit /b 1
)

if not exist "pyproject.toml" (
    echo ❌ pyproject.toml not found. Please run this script from the project root directory.
    pause
    exit /b 1
)

echo ✅ Project files found

REM Install dependencies if needed
echo 📦 Checking dependencies...
if not exist ".venv" (
    echo 🔧 Creating virtual environment and installing dependencies...
    uv sync
) else (
    echo ✅ Virtual environment exists
    REM Check if dependencies are up to date
    echo 🔄 Syncing dependencies...
    uv sync
)

echo 🚀 Starting Temperature Trends Viz...
echo 📱 The application will open in your default browser
echo 🛑 Press Ctrl+C to stop the application
echo.

REM Run the application
uv run streamlit run weather_gui.py

echo.
echo 👋 Thanks for using Temperature Trends Viz!
pause
