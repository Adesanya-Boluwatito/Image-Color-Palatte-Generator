# Image Color Palette Generator

A web application that extracts and displays the top 10 most common colors from uploaded images, similar to [Flat UI Colors](https://flatuicolors.com/) and [Cool PHP Tools Color Extract](http://www.coolphptools.com/color_extract).

![Image Color Palette Generator Screenshot](static/screenshot.png)

## Features

- Upload images (JPG, PNG, GIF) to extract color palettes
- View the top 10 most dominant colors in the image
- Display colors with their HEX codes
- Copy color codes to clipboard with a single click
- Responsive design for desktop and mobile devices

## How It Works

The application uses:
- **Flask** as the web framework
- **PIL (Pillow)** for image processing and color extraction
- Modern HTML, CSS, and JavaScript for the frontend

## Project Structure

```
image-color-palette-generator/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css       # CSS styles
│   ├── js/
│   │   └── script.js       # Frontend JavaScript
│   └── uploads/            # Directory for uploaded images
└── templates/
    └── index.html          # HTML template
```

## Technical Implementation

### Backend (Python/Flask)

The color extraction process works as follows:

1. The uploaded image is resized to 150x150 pixels for faster processing
2. The image is converted to RGB format if needed
3. PIL's quantize method is used to reduce the number of colors in the image
4. The most common colors are counted and extracted
5. The RGB values are converted to HEX format
6. The colors are sent back to the frontend as JSON

### Frontend (HTML/CSS/JavaScript)

The frontend:
1. Provides a simple form for image upload
2. Displays a loading spinner during processing
3. Shows the uploaded image and extracted colors
4. Allows users to click on colors to copy their HEX codes
5. Provides visual feedback when a color is copied

## Installation and Setup

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Local Development

1. Clone the repository:
   ```
   git clone <repository-url>
   cd image-color-palette-generator
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Run the application:
   ```
   python app.py
   ```

6. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Deployment to Render

[Render](https://render.com/) is a cloud platform that makes it easy to deploy web applications. Here's how to deploy this application to Render:

### Step 1: Prepare Your Application for Deployment

1. Create a `render.yaml` file in the root directory:

```yaml
services:
  - type: web
    name: image-color-palette-generator
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
```

2. Create a `Procfile` in the root directory:

```
web: gunicorn app:app
```

3. Set up your `requirements.txt` file:

```
# Core dependencies
flask==2.0.1
Pillow==8.3.1
gunicorn==20.1.0
werkzeug==2.0.1
jinja2==3.0.1
itsdangerous==2.0.1
click==8.0.1
```

4. Create a `.gitignore` file:

```
venv/
__pycache__/
*.py[cod]
*$py.class
.env
static/uploads/*
!static/uploads/.gitkeep
```

5. Create an empty `.gitkeep` file in the `static/uploads` directory to ensure the directory is tracked by Git but its contents are ignored.

### Step 2: Handling Dependencies

This application uses a simple color extraction method that only relies on PIL (Pillow), which makes it easy to deploy to cloud platforms like Render. The color extraction is implemented in `simple_color_extractor.py` and uses PIL's quantize method to find the most common colors in an image.

### Step 3: Modify app.py for Production

Update your `app.py` to handle production environment:

```python
# Add at the top of app.py
import os

# Replace the last lines with:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### Step 4: Push Your Code to GitHub

1. Initialize a Git repository (if not already done):
   ```
   git init
   ```

2. Add all files:
   ```
   git add .
   ```

3. Commit changes:
   ```
   git commit -m "Initial commit"
   ```

4. Create a new repository on GitHub and push your code:
   ```
   git remote add origin <github-repository-url>
   git push -u origin main
   ```

### Step 4: Deploy on Render

1. Sign up for a [Render account](https://render.com/)
2. From the Render dashboard, click "New" and select "Web Service"
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` file and configure your service
5. Click "Create Web Service"
6. Wait for the deployment to complete (this may take a few minutes)
7. Once deployed, Render will provide a URL for your application

### Step 5: Configure Environment Variables (if needed)

If your application requires environment variables:
1. Go to your web service in the Render dashboard
2. Click on "Environment"
3. Add any required environment variables
4. Click "Save Changes"

## Customization

You can customize the application by:

1. Changing the number of colors extracted (modify the `num_colors` parameter in `extract_colors()`)
2. Adjusting the image resize dimensions for different processing speeds/accuracy
3. Modifying the CSS to change the appearance of the color palette
4. Adding additional features like color sorting or filtering

## Troubleshooting

### Common Issues

1. **Image upload fails**: Ensure the upload directory has proper permissions
2. **Color extraction is slow**: Try reducing the image resize dimensions
3. **Deployment issues**: Check Render logs for specific error messages

### Deployment Troubleshooting

If you encounter issues deploying to Render, here are some common problems and solutions:

1. **Dependency conflicts**: Make sure to specify exact versions of all dependencies in requirements.txt, including Flask's dependencies (Werkzeug, Jinja2, etc.)

2. **Build failures with NumPy or scikit-learn**: These packages require compilation and can cause issues on cloud platforms. Our application uses a simpler approach with just PIL to avoid these issues.

3. **"ImportError: cannot import name 'url_quote'"**: This is caused by a version mismatch between Flask and Werkzeug. Make sure to specify werkzeug==2.0.1 in your requirements.txt.

4. **Static files not being served**: Make sure your static directories (uploads, css, js) exist and have the correct permissions.

5. **Application crashes after deployment**: Check the Render logs for specific error messages. Common issues include missing environment variables or incorrect file paths.

## Future Enhancements

Potential improvements for the application:

1. Add color sorting options (by hue, saturation, etc.)
2. Implement color naming using a color name database
3. Add the ability to save and share color palettes
4. Implement user accounts to save favorite palettes
5. Add color scheme suggestions based on extracted colors

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by [Flat UI Colors](https://flatuicolors.com/)
- Color extraction technique based on KMeans clustering
