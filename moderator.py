import cv2
import torch
from PIL import Image
from transformers import AutoModelForImageClassification, ViTImageProcessor, pipeline

class UnifiedModerator:
    def __init__(self):
        print("[INFO] Initializing Unified Models...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # 1. VISUAL MODEL (For Images & Video)
        model_name = "Falconsai/nsfw_image_detection"
        self.img_processor = ViTImageProcessor.from_pretrained(model_name)
        self.img_model = AutoModelForImageClassification.from_pretrained(model_name).to(self.device)
        self.img_model.eval()
        
        # 2. TEXT MODEL (For Comments/Bio)
        # We load this on CPU (-1) to save GPU memory for video if needed, or change to 0 for GPU
        print("[INFO] Loading Text Toxicity Model...")
        self.text_pipe = pipeline("text-classification", model="unitary/toxic-bert", top_k=None, device=-1)
        
        print(f"[INFO] All Models Loaded on {self.device.upper()}. Ready.")

    def moderate_image(self, pil_image):
        """Helper function to check a single image"""
        inputs = self.img_processor(images=pil_image, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.img_model(**inputs)
            probs = outputs.logits.softmax(dim=1)
        
        # Label 1 is usually NSFW for this model
        nsfw_score = probs[0][1].item()
        
        if nsfw_score > 0.8:
            return {"verdict": "UNSAFE", "score": round(nsfw_score, 3), "type": "NSFW_VISUAL"}
        return {"verdict": "SAFE", "score": round(nsfw_score, 3), "type": "CLEAN"}

    def moderate_text(self, text):
        """Checks text for hate speech, insults, or threats"""
        results = self.text_pipe(text)[0]
        
        # Check if any toxic label is high
        for label in results:
            if label['score'] > 0.7: 
                return {
                    "verdict": "UNSAFE", 
                    "score": round(label['score'], 3), 
                    "type": f"TEXT_{label['label'].upper()}"
                }
        
        return {"verdict": "SAFE", "score": 0.0, "type": "CLEAN"}

    def moderate_video(self, video_path, interval=1.5):
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0: fps = 30
        step = int(fps * interval)
        if step < 1: step = 1

        unsafe_frames = []
        frame_idx = 0
        
        while True:
            if frame_idx % step != 0:
                if not cap.grab(): break
                frame_idx += 1
                continue

            ret, frame = cap.read()
            if not ret: break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_frame)
            
            result = self.moderate_image(pil_img)
            
            if result["verdict"] == "UNSAFE":
                timestamp = frame_idx / fps
                unsafe_frames.append({"time": round(timestamp, 2), "score": result["score"]})
                if len(unsafe_frames) >= 3: break
            
            frame_idx += 1
            
        cap.release()
        
        if unsafe_frames:
            return {"verdict": "UNSAFE", "flagged_segments": unsafe_frames}
        return {"verdict": "SAFE", "flagged_segments": []}