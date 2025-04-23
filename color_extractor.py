import numpy as np
from PIL import Image
from collections import Counter

def rgb_to_hex(rgb):
    """Convert RGB tuple to hexadecimal color code."""
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def extract_colors_simple(image_path, num_colors=10):
    """
    Extract dominant colors from an image without using scikit-learn.
    This is a simpler alternative that uses color quantization and counting.
    """
    # Open the image
    image = Image.open(image_path)
    
    # Resize image to speed up processing
    image = image.resize((150, 150))
    
    # Convert to RGB if it's not already
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Quantize the image to reduce the number of colors
    # This is a simple way to find dominant colors without KMeans
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

def extract_colors_kmeans(image_path, num_colors=10):
    """
    Extract dominant colors using KMeans clustering.
    This is the original implementation that uses scikit-learn.
    """
    try:
        from sklearn.cluster import KMeans
        
        # Open the image
        image = Image.open(image_path)
        
        # Resize image to speed up processing
        image = image.resize((150, 150))
        
        # Convert to RGB if it's not already
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert image to numpy array
        image_array = np.array(image)
        
        # Reshape the array to be a list of pixels
        pixels = image_array.reshape(-1, 3)
        
        # Use KMeans to find the most common colors
        kmeans = KMeans(n_clusters=num_colors)
        kmeans.fit(pixels)
        
        # Get the colors
        colors = kmeans.cluster_centers_
        
        # Convert to hex
        hex_colors = [rgb_to_hex(color) for color in colors]
        
        return hex_colors
    except ImportError:
        # Fall back to simple method if scikit-learn is not available
        return extract_colors_simple(image_path, num_colors)

def extract_colors(image_path, num_colors=10):
    """
    Main function to extract colors from an image.
    Tries to use KMeans first, falls back to simple method if needed.
    """
    try:
        return extract_colors_kmeans(image_path, num_colors)
    except Exception as e:
        print(f"Error using KMeans: {e}")
        return extract_colors_simple(image_path, num_colors)
