@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0install_voices.ps1" %*
if errorlevel 1 (
  echo.
  echo Install failed. Read the message above, then run Install.bat again - it resumes.
  pause
  exit /b 1
)
echo.
echo Install finished. You can start the game.
pause
