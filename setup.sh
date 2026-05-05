#!/bin/bash

# Setup script for CodeCtx on macOS/Linux
# Creates venv, installs dependencies, and initializes configuration

echo ""
echo "================================================"
echo "CodeCtx Setup for macOS/Linux"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9+ using:"
    echo "  macOS: brew install python3"
    echo "  Ubuntu: sudo apt-get install python3 python3-venv"
    echo "  Fedora: sudo dnf install python3"
    exit 1
fi

echo "[1/5] Python found:"
python3 --version
echo ""

# Create virtual environment
echo "[2/5] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists"
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
    echo "Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "[3/5] Activating virtual environment..."
source venv/bin/activate
echo ""

# Install requirements
echo "[4/5] Installing dependencies..."
pip install -q --upgrade pip setuptools wheel
pip install -e .
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "Dependencies installed"
echo ""

# Copy .env.example if .env doesn't exist
echo "[5/5] Setting up configuration..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "Configuration template created: .env"
    fi
fi
echo ""

# Initialize CodeCtx config
echo "Initializing CodeCtx configuration..."
python3 -m codectx --help >/dev/null
python3 -c "from codectx.config_manager import get_config_manager; cm = get_config_manager(); print('Config initialized')"
echo ""

echo "================================================"
echo "Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "  1. Edit .env if needed (optional)"
echo "  2. Run: codectx ."
echo ""
echo "To activate venv in future sessions:"
echo "  source venv/bin/activate"
echo ""
