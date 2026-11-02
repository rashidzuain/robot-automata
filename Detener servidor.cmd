@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo No se encontro el entorno del servidor.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" -m server --stop
if errorlevel 1 pause
