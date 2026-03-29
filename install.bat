@echo off
cd /d "%~dp0"
echo Création environnement...
python -m venv venv
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
echo ✓ Installation terminée!
echo Lancez: start.bat
pause
