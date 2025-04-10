#!/bin/bash

echo "Setting up Image Scraper..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Install required packages
echo "Installing required Python packages..."
pip3 install -r requirements.txt || python3 -m pip install -r requirements.txt

# Generate extension icons
echo "Generating extension icons..."
python3 generate_icons.py

echo "Setup complete!"
echo
echo "To run the server, use: python3 server.py"
echo "To use the Python script directly, use: python3 image_scraper.py [URL]"
echo
echo "To install the Chrome extension:"
echo "1. Open Chrome and go to chrome://extensions/"
echo "2. Enable \"Developer mode\""
echo "3. Click \"Load unpacked\" and select the chrome_extension folder"
echo

# Ask if user wants to start the server
read -p "Do you want to start the server now? (y/n): " start_server
if [[ $start_server == "y" || $start_server == "Y" ]]; then
    echo "Starting server..."
    python3 server.py
fi

exit 0