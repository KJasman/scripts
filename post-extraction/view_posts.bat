@echo off
REM Instagram Post Viewer - Batch launcher


cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Attempting to install...
    echo.
    
    REM Check if winget is available
    winget --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Error: Windows Package Manager ^(winget^) is not available.
        echo Please install Python manually from https://www.python.org/downloads/
        echo Make sure to check "Add Python to PATH" during installation.
        pause
        exit /b 1
    )
    
    echo Installing Python using Windows Package Manager...
    winget install Python.Python.3.12 --silent
    if %errorlevel% neq 0 (
        echo Error: Failed to install Python!
        echo Please install Python manually from https://www.python.org/downloads/
        pause
        exit /b 1
    )
    
    echo Python installed successfully!
    echo Please close this window and run the batch file again.
    pause
    exit /b 0
)

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment not found. Creating one...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
    echo.
)

REM Check if requirements need to be installed
if not exist ".venv\Scripts\pip.exe" (
    echo Error: Virtual environment is corrupted!
    pause
    exit /b 1
)

echo Checking and installing requirements...
.venv\Scripts\python.exe -m pip install --upgrade pip >nul 2>&1
.venv\Scripts\python.exe -m pip install -r src\requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install requirements!
    pause
    exit /b 1
)
echo.

REM Run the Instagram viewer
echo Starting Instagram Post Viewer...
echo.
.venv\Scripts\python.exe src\instagram_viewer.py %*

pause
