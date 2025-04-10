// Function to show status messages
function showStatus(message, type) {
  const statusElement = document.getElementById('status');
  statusElement.textContent = message;
  statusElement.className = type;
  statusElement.style.display = 'block';
}

// Function to extract images directly from the page
function extractImagesFromPage() {
  return Array.from(document.images)
    .map(img => ({
      src: img.src,
      width: img.naturalWidth || img.width,
      height: img.naturalHeight || img.height,
      alt: img.alt || ''
    }));
}

// Function to download images directly using the browser
document.getElementById('scrape-direct').addEventListener('click', async () => {
  try {
    // Get minimum dimensions from inputs
    const minWidth = parseInt(document.getElementById('min-width').value) || 0;
    const minHeight = parseInt(document.getElementById('min-height').value) || 0;
    
    // Get the active tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    // Execute script in the active tab to extract images
    const results = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: extractImagesFromPage
    });
    
    // Get the images from the results
    const images = results[0].result;
    
    // Filter images by minimum dimensions
    const filteredImages = images.filter(img => 
      img.width >= minWidth && img.height >= minHeight
    );
    
    if (filteredImages.length === 0) {
      showStatus('No images found that match your criteria.', 'error');
      return;
    }
    
    showStatus(`Found ${filteredImages.length} images. Starting download...`, 'progress');
    
    // Download each image
    let downloadCount = 0;
    for (const img of filteredImages) {
      try {
        // Create a filename from the URL
        const url = new URL(img.src);
        let filename = url.pathname.split('/').pop();
        
        // If filename is empty or doesn't have an extension, create a default one
        if (!filename || !filename.includes('.')) {
          filename = `image_${Math.floor(Math.random() * 10000)}.jpg`;
        }
        
        // Download the image
        await chrome.downloads.download({
          url: img.src,
          filename: `downloaded_images/${filename}`,
          saveAs: false
        });
        
        downloadCount++;
      } catch (err) {
        console.error(`Error downloading image: ${img.src}`, err);
      }
    }
    
    showStatus(`Successfully downloaded ${downloadCount} images.`, 'success');
  } catch (error) {
    console.error('Error:', error);
    showStatus(`Error: ${error.message}`, 'error');
  }
});

// Function to send URL to Python script
document.getElementById('scrape-python').addEventListener('click', async () => {
  try {
    // Get the active tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    // Get minimum dimensions from inputs
    const minWidth = parseInt(document.getElementById('min-width').value) || 0;
    const minHeight = parseInt(document.getElementById('min-height').value) || 0;
    
    // Create a URL with the parameters
    const url = new URL('http://localhost:5000/scrape');
    url.searchParams.append('url', tab.url);
    url.searchParams.append('min_width', minWidth);
    url.searchParams.append('min_height', minHeight);
    
    showStatus('Sending request to Python script...', 'progress');
    
    // Send request to local server
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`Server responded with status: ${response.status}`);
    }
    
    const data = await response.json();
    showStatus(`Success! Downloaded ${data.count} images to ${data.output_dir}`, 'success');
  } catch (error) {
    console.error('Error:', error);
    showStatus(`Error: ${error.message}. Make sure the Python server is running.`, 'error');
  }
});