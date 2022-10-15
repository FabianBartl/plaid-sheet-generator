@echo off
cls

@REM setup nodejs environment
call nodejs/nodevars.bat

python main.py

@REM pause