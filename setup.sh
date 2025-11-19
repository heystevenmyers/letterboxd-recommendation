#!/bin/bash
# Setup script for Letterboxd Movie Matcher
# This creates a virtual environment and installs dependencies

echo "🎬 Setting up Letterboxd Movie Matcher..."
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment."
    echo "   You may need to install Xcode command line tools:"
    echo "   xcode-select --install"
    exit 1
fi

echo "✓ Virtual environment created"
echo ""

# Activate virtual environment and install packages
echo "📥 Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Setup complete!"
    echo ""
    echo "To run the app:"
    echo "  1. Activate the virtual environment:"
    echo "     source venv/bin/activate"
    echo ""
    echo "  2. Start the server:"
    echo "     cd backend"
    echo "     python app.py"
    echo ""
    echo "  3. Open http://localhost:5000 in your browser"
else
    echo ""
    echo "❌ Failed to install dependencies"
    exit 1
fi

