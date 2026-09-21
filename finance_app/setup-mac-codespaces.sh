#!/usr/bin/env bash

echo "🚀 Setting up SproutFinance for macOS & Codespaces..."

# 1. Create virtual environment
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✅ Virtual environment (.venv) created."
fi

# 2. Activate virtual environment
source .venv/bin/activate

# 3. Upgrade pip and install dependencies
pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    pip install reflex
fi

echo "✅ Dependencies installed."

# 4. Initialize Reflex if needed
if [ ! -d ".reflex" ]; then
    reflex init
fi

echo "▶️ Launching SproutFinance server..."
reflex run