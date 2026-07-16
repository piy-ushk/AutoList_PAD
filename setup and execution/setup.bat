@echo off
chcp 65001 >nul
cd /d "%~dp0.."

echo ==========================================
echo AutoList - Initial Setup (初期設定)
echo ==========================================
echo.
echo Installing required Python libraries...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.
echo ==========================================
echo Running Google Authentication...
echo A browser window will open. Please log in to your Google Account.
echo ==========================================
python modules\gsheets.py
echo.
echo Setup Complete! You can close this window.
pause
