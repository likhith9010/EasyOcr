# Use Python 3.11 slim image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install PyTorch CPU-only version (smaller size)
RUN pip install --no-cache-dir torch==2.1.0+cpu torchvision==0.16.0+cpu --index-url https://download.pytorch.org/whl/cpu

# Install other dependencies
RUN pip install --no-cache-dir Flask==3.0.0 easyocr==1.7.1 Pillow==10.1.0 reportlab==4.0.7 gunicorn==21.2.0 flask-cors==4.0.0 opencv-python-headless==4.8.1.78

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p uploads extracted_texts

# Expose port
EXPOSE 8080

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "300", "--workers", "1", "api:app"]
