import shutil
import os
import io
from PIL import Image
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import RedirectResponse

# Import your custom classes
from video_moderator import VideoModerator
from text_moderator import TextModerator

app = FastAPI()

print("--- SYSTEM STARTUP ---")
print("[INFO] Initializing AI Models (This takes a few seconds)...")

# 1. Load Text Model
text_mod = TextModerator()

# 2. Load Video Model 
# (This automatically loads the Image/CLIP models inside it, saving RAM)
video_mod = VideoModerator()

print("[INFO] AI Models Ready! Server is running.")

# --- ROUTE 0: ROOT (Redirect to Docs) ---
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

# --- ROUTE 1: TEXT ---
@app.post("/moderate/text")
async def check_text(caption: str):
    # We use the text model to predict
    verdict = text_mod.predict(caption)
    return {"verdict": verdict}

# --- ROUTE 2: IMAGE ---
@app.post("/moderate/image")
async def check_image(file: UploadFile = File(...)):
    try:
        # Read the image bytes asynchronously
        image_data = await file.read()
        pil_image = Image.open(io.BytesIO(image_data))
        
        # Reuse the model loaded inside video_mod
        verdict, score = video_mod.img_mod.predict(pil_image)
        
        return {
            "filename": file.filename,
            "verdict": verdict,
            "score": round(score, 3)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image Error: {str(e)}")

# --- ROUTE 3: VIDEO ---
@app.post("/moderate/video")
async def check_video(file: UploadFile = File(...)):
    # 1. Save video to temp file
    temp_filename = f"temp_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # 2. Run the video moderation logic
        verdict = video_mod.process_video(temp_filename)
        
        # 3. Cleanup (Delete temp file)
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        
        return {"filename": file.filename, "verdict": verdict}
    
    except Exception as e:
        # Cleanup if crash
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        raise HTTPException(status_code=500, detail=f"Video Error: {str(e)}")

# Command to run:
# uvicorn api:app --reload