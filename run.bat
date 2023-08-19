@echo off
call python .\src\checkModule.py
call python .\src\main.py
if %errorlevel%==1 (
    call python .\src\update\update.py
    .\run.bat
)
pause
