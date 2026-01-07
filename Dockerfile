# Use Python 3.9
FROM python:3.9-slim

# Install system dependencies required for OpenCV
# FIX: Changed 'libgl1-mesa-glx' to 'libgl1' because the old one is deprecated
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Create a writable cache directory for the AI model
RUN mkdir -p /app/.cache && chmod 777 /app/.cache
ENV XDG_CACHE_HOME=/app/.cache

# Start the server on port 7860
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "7860"]