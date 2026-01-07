from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import shutil
import os
from PIL import Image
import io
from moderator import UnifiedModerator

app = FastAPI(title="Unified Content Safety API")

# Initialize logic
print("[INFO] Initializing Unified Gateway...")
mod = UnifiedModerator()

# --- Request Models ---
class TextRequest(BaseModel):
    text: str

# --- Routes ---

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.post("/moderate/text")
async def check_text(payload: TextRequest):
    """Checks comments, bios, or captions for toxicity"""
    result = mod.moderate_text(payload.text)
    return result

@app.post("/moderate/image")
async def check_image(file: UploadFile = File(...)):
    """Checks a single image file (JPG/PNG)"""
    # Read image bytes directly (no need to save to disk)
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    
    result = mod.moderate_image(image)
    return result

@app.post("/moderate/video")
async def check_video(file: UploadFile = File(...)):
    """Checks a video file"""
    temp_filename = f"temp_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result = mod.moderate_video(temp_filename)
        return result
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)