from PIL import Image
from collections import Counter

def rgb_to_hex(rgb):
    """Convert RGB tuple to hexadecimal color code."""
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def extract_colors(image_path, num_colors=10):
    """
    Extract dominant colors from an image using only PIL.
    This is a simple implementation that doesn't require NumPy or scikit-learn.
    """
    # Open the image
    image = Image.open(image_path)
    
    # Resize image to speed up processing
    image = image.resize((150, 150))
    
    # Convert to RGB if it's not already
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Quantize the image to reduce the number of colors
    # This is a simple way to find dominant colors
    quantized = image.quantize(colors=64, method=2)
    
    # Convert back to RGB for processing
    quantized_rgb = quantized.convert('RGB')
    
    # Get pixel data
    pixels = list(quantized_rgb.getdata())
    
    # Count occurrences of each color
    color_counts = Counter(pixels)
    
    # Get the most common colors
    most_common = color_counts.most_common(num_colors)
    
    # Convert to hex
    hex_colors = [rgb_to_hex(color) for color, count in most_common]
    
    return hex_colors
