from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, output_path):
    """Create a simple icon with the given size."""
    # Create a new image with a white background
    img = Image.new('RGBA', (size, size), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a blue circle as the background
    circle_margin = size // 10
    circle_size = size - (2 * circle_margin)
    draw.ellipse(
        [(circle_margin, circle_margin), 
         (circle_margin + circle_size, circle_margin + circle_size)],
        fill=(66, 133, 244, 255)  # Google blue
    )
    
    # Draw a white "IS" text (for Image Scraper)
    # Try to use a built-in font that should be available on most systems
    try:
        # For larger icons, try to use a font
        if size >= 48:
            font_size = size // 3
            try:
                font = ImageFont.truetype("Arial", font_size)
            except IOError:
                # Fallback to default font
                font = ImageFont.load_default()
            
            # Calculate text position to center it
            text = "IS"
            text_width, text_height = draw.textsize(text, font=font) if hasattr(draw, 'textsize') else (font_size, font_size)
            position = ((size - text_width) // 2, (size - text_height) // 2)
            
            # Draw the text
            draw.text(position, text, fill=(255, 255, 255, 255), font=font)
        else:
            # For small icons, just draw a white dot in the center
            center_dot_size = size // 4
            center = size // 2
            draw.ellipse(
                [(center - center_dot_size//2, center - center_dot_size//2),
                 (center + center_dot_size//2, center + center_dot_size//2)],
                fill=(255, 255, 255, 255)
            )
    except Exception as e:
        print(f"Error adding text to icon: {e}")
        # If text drawing fails, just leave the blue circle
    
    # Save the image
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    print(f"Created icon: {output_path}")

def main():
    # Create icons in different sizes
    create_icon(16, "chrome_extension/icon16.png")
    create_icon(48, "chrome_extension/icon48.png")
    create_icon(128, "chrome_extension/icon128.png")

if __name__ == "__main__":
    main()