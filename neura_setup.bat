@echo off
cd /d "%~dp0"
setlocal enabledelayedexpansion

chcp 65001 >nul


color 0A

echo.
echo ============================ NEURA AUTO SETUP AUTHORITY ============================
echo.

py -3.10 --version >nul 2>&1
if !errorlevel! neq 0 (
    echo Python 3.10 not found. Downloading installer...
    curl -L -o python_installer.exe https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe
    if !errorlevel! neq 0 (
        echo Failed to download Python. Please install it manually from python.org
        pause
        exit /b 1
    )
    
    echo Installing Python 3.10 ^(this may take a minute^)... 
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe

    set "PATH=%PATH%;%ProgramFiles%\Python310\;%ProgramFiles%\Python310\Scripts\"
    
    py -3.10 --version >nul 2>&1
    if !errorlevel! neq 0 (
        echo Python installation failed or path not refreshed.
        echo Please restart your terminal after installation.
        pause
        exit /b 1
    )
) else (
    echo Python 3.10 is already installed.
)

echo Installing dependencies...
py -3.10 -m pip install --upgrade pip --quiet
py -3.10 -m pip install -r requirements.txt --quiet
if !errorlevel! neq 0 (
    echo Failed to install dependencies. Check your internet connection.
    pause
    exit /b 1
)
echo Dependencies installed successfully.

py -3.10 config_helper.py
if !errorlevel! neq 0 (
    echo Configuration helper failed.
    pause
    exit /b 1
)

echo Setup complete! Starting Neura-Self...
echo.
py -3.10 main.py

pause
