# Use Python 3.9
FROM python:3.9-slim

# Install system dependencies required for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Create a writable cache directory for the AI model
# (Hugging Face needs permission to download the model here)
RUN mkdir -p /app/.cache && chmod 777 /app/.cache
ENV XDG_CACHE_HOME=/app/.cache

# Start the server on port 7860
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "7860"]