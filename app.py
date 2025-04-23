import os
import numpy as np
from flask import Flask, render_template, request, jsonify
from PIL import Image
from collections import Counter
from sklearn.cluster import KMeans

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def extract_colors(image_path, num_colors=10):
    # Open the image
    image = Image.open(image_path)

    # Resize image to speed up processing
    image = image.resize((150, 150))

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        # Create uploads directory if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Save the file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Extract colors
        colors = extract_colors(file_path)

        return jsonify({
            'colors': colors,
            'image_path': file_path
        })

    return jsonify({'error': 'File type not allowed'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
