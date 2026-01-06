from fastapi import FastAPI, UploadFile, File
from fastapi.responses import RedirectResponse # <--- NEW IMPORT
import shutil
import os
from moderator import FastVideoModerator

app = FastAPI()

# Initialize the correct class
print("[INFO] Initializing server...")
moderator = FastVideoModerator(frame_interval=1.5, confidence_threshold=0.75)

# --- NEW: Redirect Homepage to Docs ---
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")
# --------------------------------------

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
    print("[INFO] Starting server on port 7860...")
    uvicorn.run(app, host="0.0.0.0", port=7860)