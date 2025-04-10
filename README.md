# Image Scraper

This tool helps you scrape and download images from web pages. It provides two ways to use it:

1. A Python script that can be run from the command line
2. A Chrome extension that integrates with your browser

## Setup

### Prerequisites

- Python 3.7 or higher
- Google Chrome browser (for the extension)

### Installation

1. Clone or download this repository
2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Generate the extension icons:

```bash
python generate_icons.py
```

## Using the Python Script Directly

You can use the Python script directly from the command line:

```bash
python image_scraper.py https://example.com/page-with-images --output ./downloaded_images
```

### Options:

- `--output` or `-o`: Directory to save downloaded images (default: ./downloaded_images)
- `--min-width`: Minimum width of images to download (default: 0)
- `--min-height`: Minimum height of images to download (default: 0)

Example with filters:

```bash
python image_scraper.py https://example.com --min-width 500 --min-height 500
```

## Using the Chrome Extension

### Installing the Extension

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in the top-right corner)
3. Click "Load unpacked" and select the `chrome_extension` folder from this repository

### Using the Extension

The extension provides two ways to download images:

#### 1. Direct Download

This method uses Chrome's built-in capabilities to download images directly:

1. Navigate to the web page containing the images you want to download
2. Click the Image Scraper extension icon in your browser toolbar
3. (Optional) Set minimum dimensions for the images
4. Click "Download Images Directly"
5. Images will be downloaded to your default Chrome downloads folder

#### 2. Using the Python Script (Advanced)

This method provides more advanced features by using the Python script:

1. Start the server:

```bash
python server.py
```

2. Navigate to the web page containing the images
3. Click the Image Scraper extension icon
4. (Optional) Set minimum dimensions
5. Click "Download with Python Script"
6. Images will be downloaded to the `downloaded_images` folder in this repository

## Troubleshooting

- If the "Download with Python Script" option doesn't work, make sure the server is running (`python server.py`)
- If no images are downloaded, try adjusting the minimum width and height settings
- For websites that load images dynamically, the Python script may be more effective than the direct download option

## License

This project is open source and available under the MIT License.