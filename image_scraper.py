import os
import time
import argparse
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from PIL import Image
from io import BytesIO

def setup_driver():
    """Set up and return a Chrome WebDriver instance."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (optional)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_page_source(url):
    """Get the HTML source of a webpage using Selenium."""
    driver = setup_driver()
    try:
        driver.get(url)
        # Wait for page to load completely
        time.sleep(3)
        page_source = driver.page_source
        return page_source
    finally:
        driver.quit()

def extract_images(html, base_url):
    """Extract image URLs from HTML content."""
    soup = BeautifulSoup(html, 'html.parser')
    img_tags = soup.find_all('img')
    
    image_urls = []
    for img in img_tags:
        # Get image URL from src or data-src attribute
        img_url = img.get('src') or img.get('data-src')
        if img_url:
            # Convert relative URLs to absolute URLs
            img_url = urljoin(base_url, img_url)
            # Filter out base64 encoded images
            if not img_url.startswith('data:'):
                image_urls.append(img_url)
    
    return image_urls

def download_image(url, save_dir, filename=None):
    """Download an image from a URL and save it to disk."""
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        
        # Generate filename if not provided
        if not filename:
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename or '.' not in filename:
                # If filename is empty or has no extension, create a default one
                filename = f"image_{hash(url) % 10000}.jpg"
        
        # Ensure the file has an extension
        if '.' not in filename:
            filename += '.jpg'
        
        # Save the image
        img_path = os.path.join(save_dir, filename)
        
        # Verify it's actually an image by opening it with PIL
        img = Image.open(BytesIO(response.content))
        img.save(img_path)
        
        return img_path
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Scrape images from a webpage')
    parser.add_argument('url', help='URL of the webpage to scrape')
    parser.add_argument('--output', '-o', default='./downloaded_images', 
                        help='Directory to save downloaded images')
    parser.add_argument('--min-width', type=int, default=0,
                        help='Minimum width of images to download')
    parser.add_argument('--min-height', type=int, default=0,
                        help='Minimum height of images to download')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    print(f"Scraping images from: {args.url}")
    html = get_page_source(args.url)
    image_urls = extract_images(html, args.url)
    
    print(f"Found {len(image_urls)} images")
    
    # Download images
    downloaded_count = 0
    for i, img_url in enumerate(image_urls):
        print(f"Downloading image {i+1}/{len(image_urls)}: {img_url}")
        img_path = download_image(img_url, args.output)
        if img_path:
            downloaded_count += 1
    
    print(f"Successfully downloaded {downloaded_count} images to {args.output}")

if __name__ == "__main__":
    main()