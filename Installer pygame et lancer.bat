@echo off
cd /d "%~dp0"
echo Installation des dependances dans venv311 (si le dossier existe)...
if exist "venv311\Scripts\python.exe" (
    "venv311\Scripts\python.exe" -m pip install --upgrade pip
    "venv311\Scripts\python.exe" -m pip install -r requirements.txt
    echo.
    echo Lancement du jeu...
    "venv311\Scripts\python.exe" main.py
) else (
    echo venv311 introuvable. Creation avec Python 3.11...
    py -3.11 -m venv venv311
    if errorlevel 1 (
        echo Echec. Installe Python 3.11 depuis python.org puis relance ce script.
        pause
        exit /b 1
    )
    "venv311\Scripts\python.exe" -m pip install --upgrade pip
    "venv311\Scripts\python.exe" -m pip install -r requirements.txt
    "venv311\Scripts\python.exe" main.py
)
pause
