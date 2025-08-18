#!/bin/bash

echo "========================================"
echo "    AI Voice Assistant Launcher"
echo "========================================"
echo

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7+ from https://python.org"
    exit 1
fi

echo "Python found! Checking dependencies..."
echo

echo "Installing/updating required packages..."
pip3 install -r requirements.txt

echo
echo "========================================"
echo "Starting AI Voice Assistant..."
echo "========================================"
echo
echo "Say 'quit' or 'goodbye' to exit"
echo "Continuous listening mode enabled"
echo
echo "Press Enter to start..."
read

python3 voice_assistant.py

echo
echo "Assistant stopped. Press Enter to exit..."
read
