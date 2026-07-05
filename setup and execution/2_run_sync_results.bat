@echo off
chcp 65001 >nul
cd /d "%~dp0.."

echo ==========================================
echo AutoList - Step 2: Sync Results
echo ==========================================
echo.
echo Syncing PAD results back to Google Sheets...
python sync_results.py
echo.
echo ==========================================
echo Sync Complete! Daily operations finished.
echo ==========================================
pause
