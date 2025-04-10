import os
import subprocess
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/scrape', methods=['GET'])
def scrape_images():
    # Get parameters from request
    url = request.args.get('url')
    min_width = request.args.get('min_width', '0')
    min_height = request.args.get('min_height', '0')
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloaded_images')
    
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400
    
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Build command to run image_scraper.py
        cmd = [
            'python', 'image_scraper.py', 
            url, 
            '--output', output_dir,
            '--min-width', min_width,
            '--min-height', min_height
        ]
        
        # Run the command
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            return jsonify({
                'error': f'Script execution failed: {result.stderr}'
            }), 500
        
        # Count files in output directory
        image_count = len([f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))])
        
        return jsonify({
            'success': True,
            'count': image_count,
            'output_dir': output_dir,
            'message': result.stdout
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)