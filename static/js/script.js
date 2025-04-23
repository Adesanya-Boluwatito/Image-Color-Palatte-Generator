document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const fileInput = document.getElementById('file-input');
    const resultsContainer = document.getElementById('results-container');
    const imagePreview = document.getElementById('image-preview');
    const colorPalette = document.getElementById('color-palette');
    const loading = document.getElementById('loading');
    
    // Handle file input change to show file name
    fileInput.addEventListener('change', function() {
        const fileName = this.files[0]?.name || 'No file chosen';
        const label = document.querySelector('.file-input-label');
        label.textContent = fileName;
    });
    
    // Handle form submission
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        
        // Check if a file was selected
        if (!fileInput.files.length) {
            alert('Please select an image file');
            return;
        }
        
        // Show loading spinner
        loading.style.display = 'block';
        resultsContainer.style.display = 'none';
        
        // Send the file to the server
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Hide loading spinner
            loading.style.display = 'none';
            
            if (data.error) {
                alert(data.error);
                return;
            }
            
            // Show results
            resultsContainer.style.display = 'block';
            
            // Display the image
            imagePreview.innerHTML = `<img src="${data.image_path}" alt="Uploaded Image">`;
            
            // Display the color palette
            colorPalette.innerHTML = '';
            data.colors.forEach(color => {
                const colorBox = document.createElement('div');
                colorBox.className = 'color-box';
                colorBox.style.backgroundColor = color;
                
                // Determine if text should be white or black based on color brightness
                const r = parseInt(color.slice(1, 3), 16);
                const g = parseInt(color.slice(3, 5), 16);
                const b = parseInt(color.slice(5, 7), 16);
                const brightness = (r * 299 + g * 587 + b * 114) / 1000;
                const textColor = brightness > 128 ? 'black' : 'white';
                
                colorBox.style.color = textColor;
                
                colorBox.innerHTML = `
                    <div class="hex-code">${color}</div>
                    <div class="copied">Copied!</div>
                `;
                
                // Add click event to copy color code
                colorBox.addEventListener('click', function() {
                    navigator.clipboard.writeText(color).then(() => {
                        const copied = this.querySelector('.copied');
                        copied.classList.add('show');
                        setTimeout(() => {
                            copied.classList.remove('show');
                        }, 1500);
                    });
                });
                
                colorPalette.appendChild(colorBox);
            });
        })
        .catch(error => {
            loading.style.display = 'none';
            alert('An error occurred: ' + error);
        });
    });
});
