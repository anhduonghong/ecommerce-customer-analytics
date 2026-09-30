@echo off
REM Task Scheduler gọi file này. Chỉnh đường dẫn venv nếu bạn dùng tên khác.
cd /d %~dp0
call .venv\Scripts\activate.bat
python -m src.pipeline
pause
