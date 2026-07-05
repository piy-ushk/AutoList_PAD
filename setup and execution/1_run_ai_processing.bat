@echo off
chcp 65001 >nul
cd /d "%~dp0.."

echo ==========================================
echo AutoList - Step 1: AI Data Generation
echo ==========================================
echo.
echo Reading spreadsheet and generating Item Specifics...
python main.py
echo.
echo ==========================================
echo Processing Complete!
echo You may now run the Power Automate Desktop (PAD) flow.
echo ==========================================
pause
