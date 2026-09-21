@echo off
echo 🚀 Setting up SproutFinance for Windows...

:: 1. Create virtual environment
if not exist ".venv" (
    python -m venv .venv
    echo ✅ Virtual environment (.venv) created.
)

:: 2. Activate virtual environment
call .venv\Scripts\activate.bat

:: 3. Upgrade pip and install dependencies
python -m pip install --upgrade pip

if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    pip install reflex
)

echo ✅ Dependencies installed.

:: 4. Initialize Reflex if needed
if not exist ".reflex" (
    call reflex init
)

echo ▶️ Launching SproutFinance server...
call reflex run
