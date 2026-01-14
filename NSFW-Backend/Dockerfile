# Use Python 3.9
FROM python:3.9

# Set working directory
WORKDIR /code

# Install Linux dependencies for OpenCV (The "libgl1" fix)
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy all python files
COPY . .

# Create a writable directory for temp video uploads
RUN mkdir -p /code/temp && chmod 777 /code/temp

# Start the Server
# Note: Hugging Face expects the app to run on port 7860
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]