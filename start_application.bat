@echo off
cd /d "%~dp0"
echo Activating virtual environment...
call .\.venv\Scripts\activate
echo Starting the application...
python .\src\main.py
echo Deactivating virtual environment...
deactivate
echo Done.
pause