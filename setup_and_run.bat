@echo off
echo Setting up Image Scraper...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.7 or higher.
    exit /b 1
)

REM Install required packages
echo Installing required Python packages...
pip install -r requirements.txt

REM Generate extension icons
echo Generating extension icons...
python generate_icons.py

echo Setup complete!
echo.
echo To run the server, use: python server.py
echo To use the Python script directly, use: python image_scraper.py [URL]
echo.
echo To install the Chrome extension:
echo 1. Open Chrome and go to chrome://extensions/
echo 2. Enable "Developer mode"
echo 3. Click "Load unpacked" and select the chrome_extension folder
echo.

REM Ask if user wants to start the server
set /p start_server="Do you want to start the server now? (y/n): "
if /i "%start_server%"=="y" (
    echo Starting server...
    python server.py
)

exit /b 0