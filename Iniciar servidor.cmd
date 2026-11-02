@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Falta preparar Python. Segui los pasos de README.md.
  pause
  exit /b 1
)
echo Robot Automata - servidor local
echo Panel: http://127.0.0.1:8000
echo Para detenerlo, presiona Ctrl+C en esta ventana.
".venv\Scripts\python.exe" -m server
if errorlevel 1 (
  echo Si el puerto 8000 esta ocupado, comproba si el panel ya esta abierto.
  pause
)
