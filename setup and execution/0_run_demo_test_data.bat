@echo off
chcp 65001 >nul
cd /d "%~dp0.."

echo ==========================================
echo AutoList - Step 0: Insert Demo Data (UAT Test)
echo ==========================================
echo.
echo Inserting 14 test items into the Google Sheet...
python insert_final_demo.py
echo.
echo ==========================================
echo Insertion Complete! 
echo You may now double-click '1_run_ai_processing.bat' to process them.
echo ==========================================
pause
