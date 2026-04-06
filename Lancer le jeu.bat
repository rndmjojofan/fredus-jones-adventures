@echo off
REM Lance le jeu depuis le dossier du script (évite les erreurs config / assets)
cd /d "%~dp0"

if exist "venv311\Scripts\python.exe" (
    echo Utilisation de venv311 (Python 3.11 + pygame)...
    "venv311\Scripts\python.exe" main.py
) else if exist "venv\Scripts\python.exe" (
    echo Utilisation de venv...
    "venv\Scripts\python.exe" main.py
) else (
    echo Aucun venv trouve : tentative avec python du PATH...
    python main.py
)

if errorlevel 1 pause
