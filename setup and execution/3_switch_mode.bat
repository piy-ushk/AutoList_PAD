@echo off
chcp 65001 >nul
cd /d "%~dp0.."

echo ==========================================
echo AutoList - Step 3: Switch Mode (Demo / Live)
echo ==========================================
echo.
python scripts\switch_mode.py
echo.
pause
