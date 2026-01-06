import cv2
import torch
from PIL import Image
from transformers import AutoModelForImageClassification, ViTImageProcessor
import time

class FastVideoModerator:
    def __init__(self, frame_interval=2.0, confidence_threshold=0.8):
        print("[INFO] Loading FalconAI NSFW Classifier (ViT)...")
        # Load model explicitly on CPU (or GPU if available)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        model_name = "Falconsai/nsfw_image_detection"
        
        self.processor = ViTImageProcessor.from_pretrained(model_name)
        self.model = AutoModelForImageClassification.from_pretrained(model_name).to(self.device)
        self.model.eval() # Set to evaluation mode for speed

        self.frame_interval = frame_interval # Process 1 frame every X seconds
        self.threshold = confidence_threshold
        print(f"[INFO] Model Loaded on {self.device.upper()}. Ready.")

    def predict_frame(self, frame):
        """
        Resize and predict a single frame. 
        Returns (is_nsfw, score, label)
        """
        # 1. Resize small (224x224) - CRITICAL for speed
        # We use PIL because HuggingFace processors expect PIL images
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame_rgb)
        
        # 2. Process
        inputs = self.processor(images=pil_image, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = outputs.logits.softmax(dim=1)
        
        # 3. Get results
        # The model classes are usually: {0: 'normal', 1: 'nsfw'}
        score_nsfw = probs[0][1].item() # Probability of being NSFW
        score_normal = probs[0][0].item()
        
        if score_nsfw > self.threshold:
            return True, score_nsfw, "NSFW"
        else:
            return False, score_nsfw, "Normal"

    def process_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return {"error": "Could not open video"}

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0: fps = 30
        
        # Skip logic: process 1 frame every X seconds
        step = int(fps * self.frame_interval)
        if step < 1: step = 1

        print(f"[START] Processing {video_path}...")
        start_time = time.time()
        
        nsfw_frames = []
        checked_frames = 0
        current_idx = 0

        while True:
            # Efficient skipping: grab() is faster than read() for skipping
            if current_idx % step != 0:
                ret = cap.grab()
                if not ret: break
                current_idx += 1
                continue

            # Fully decode only the frames we need
            ret, frame = cap.read()
            if not ret: break

            checked_frames += 1
            
            # Predict
            is_nsfw, score, label = self.predict_frame(frame)
            
            if is_nsfw:
                timestamp = current_idx / fps
                print(f"  [!] NSFW detected at {timestamp:.1f}s (Score: {score:.2f})")
                nsfw_frames.append({
                    "timestamp": round(timestamp, 2),
                    "score": round(score, 3),
                    "label": label
                })
                
                # EARLY EXIT: If we find distinct NSFW content effectively, 
                # we can stop to save time. 
                # (Optional: Remove this 'if' to scan full video)
                if len(nsfw_frames) >= 3: 
                    print("[STOP] Multiple NSFW frames found. Early exit.")
                    break

            current_idx += 1

        cap.release()
        total_time = time.time() - start_time
        
        # Final Verdict
        is_unsafe = len(nsfw_frames) > 0
        verdict = "UNSAFE" if is_unsafe else "SAFE"
        
        return {
            "verdict": verdict,
            "processed_frames": checked_frames,
            "nsfw_frame_count": len(nsfw_frames),
            "process_time_seconds": round(total_time, 2),
            "flagged_segments": nsfw_frames
        }