#!/bin/bash

# Setup script for CodeCtx on macOS/Linux
# Delegates setup to the cross-platform bootstrap.

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
echo "[2/2] Running smart bootstrap..."
python3 bootstrap.py
if [ $? -ne 0 ]; then
    echo "ERROR: Bootstrap failed"
    exit 1
fi
echo ""

echo "================================================"
echo "Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "  1. Edit .env if needed (optional)"
echo "  2. Open a new terminal if PATH was updated"
echo "  3. Run: codectx ."
echo ""
echo "Project launcher directory:"
echo "  $PWD/bin"
echo ""
