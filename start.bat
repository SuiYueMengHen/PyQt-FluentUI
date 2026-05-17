@echo off
cd /d "%~dp0"
set QSG_RHI_BACKEND=software
call .venv\Scripts\activate.bat
python app\main.py
pause
