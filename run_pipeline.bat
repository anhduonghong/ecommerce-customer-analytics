@echo off
cd /d %~dp0
call .venv\Scripts\activate.bat
python -m src.pipeline
exit /b %ERRORLEVEL%
