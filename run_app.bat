@echo off
setlocal

echo ========================================
echo   Incident Observability
echo ========================================
echo.

where py >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python launcher "py" is not available.
    echo Install Python from https://www.python.org/downloads/
    echo and enable the Python launcher during setup.
    echo.
    pause
    exit /b 1
)

py -3.14 --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.14 was not found.
    echo.
    pause
    exit /b 1
)

echo Python 3.14 found!
echo.

if not exist .venv (
    echo Creating virtual environment...
    py -3.14 -m venv .venv
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to create virtual environment
        echo.
        pause
        exit /b 1
    )
)

if not exist .venv\Scripts\python.exe (
    echo.
    echo ERROR: Virtual environment was not created correctly
    echo.
    pause
    exit /b 1
)

echo Checking required packages...
call .venv\Scripts\python.exe -c "import openpyxl, xlrd" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing supported dependencies...
    echo.
    call .venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
    call .venv\Scripts\python.exe -m pip install --only-binary=:all: openpyxl==3.1.2 xlrd==2.0.1
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install required packages
        echo.
        pause
        exit /b 1
    )
)

echo Starting Incident Evaluator...
echo.

call .venv\Scripts\python.exe main.py

if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start
    echo Check the error messages above
    echo.
)

pause

@REM Made with Bob
