@echo off
cd /d "%~dp0"
python -m pip install -r requirements.txt --quiet --disable-pip-version-check
if errorlevel 1 (
    pause
    exit /b 1
)
cls
python main.py
pause
