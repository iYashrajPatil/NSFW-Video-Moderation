from fastapi import FastAPI, UploadFile, File
import shutil
import os
# CHANGE 1: Import the correct class name
from moderator import FastVideoModerator

app = FastAPI()

# CHANGE 2: Initialize the correct class
# Load model once at startup
print("[INFO] Initializing server...")
moderator = FastVideoModerator(frame_interval=1.5, confidence_threshold=0.75)

@app.post("/check_video")
async def check_video(file: UploadFile = File(...)):
    temp_filename = f"temp_{file.filename}"
    
    # Save Upload
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Run Check
        result = moderator.process_video(temp_filename)
        return result
    finally:
        # Clean up the file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

if __name__ == "__main__":
    import uvicorn
    print("[INFO] Starting server on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)