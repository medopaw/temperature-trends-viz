#!/bin/bash

# Temperature Trends Viz - Startup Script
# This script simplifies running the application with uv

set -e  # Exit on any error

echo "🌡️  Temperature Trends Viz Startup Script"
echo "=========================================="

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "   Or visit: https://docs.astral.sh/uv/"
    exit 1
fi

echo "✅ uv found: $(uv --version)"

# Check if we're in the right directory
if [ ! -f "weather_gui.py" ]; then
    echo "❌ weather_gui.py not found. Please run this script from the project root directory."
    exit 1
fi

if [ ! -f "pyproject.toml" ]; then
    echo "❌ pyproject.toml not found. Please run this script from the project root directory."
    exit 1
fi

echo "✅ Project files found"

# Install dependencies if needed
echo "📦 Checking dependencies..."
if [ ! -d ".venv" ]; then
    echo "🔧 Creating virtual environment and installing dependencies..."
    uv sync
else
    echo "✅ Virtual environment exists"
    # Check if dependencies are up to date
    echo "🔄 Syncing dependencies..."
    uv sync
fi

echo "🚀 Starting Temperature Trends Viz..."
echo "📱 The application will open in your default browser"
echo "🛑 Press Ctrl+C to stop the application"
echo ""

# Run the application
uv run streamlit run weather_gui.py

echo ""
echo "👋 Thanks for using Temperature Trends Viz!"
