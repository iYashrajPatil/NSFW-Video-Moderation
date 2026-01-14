# video_moderator.py
import cv2
from PIL import Image
from image_moderator import ImageModerator
import logging

class VideoModerator:
    def __init__(self):
        print("[INFO] Initializing Video Logic...")
        self.img_mod = ImageModerator()

    def process_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0: fps = 30
        
        # OPTIMIZATION 1: Check 1 frame every 2 seconds
        frame_interval = int(fps * 2) 
        if frame_interval < 1: frame_interval = 1
        
        nsfw_count = 0
        review_count = 0
        total_frames_checked = 0
        
        # OPTIMIZATION 2: Stop after 3 bad frames
        MAX_BAD_FRAMES = 3 
        
        frame_idx = 0
        final_verdict = "SAFE"

        print(f"[INFO] Scanning video: {video_path}")

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_idx % frame_interval == 0:
                total_frames_checked += 1
                
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(rgb_frame)
                
                verdict, score = self.img_mod.predict(pil_img)
                
                if verdict == "NSFW":
                    nsfw_count += 1
                    print(f"   [!] Frame {frame_idx}: ❌ NSFW (Score: {score:.2f}) | Count: {nsfw_count}/{MAX_BAD_FRAMES}")
                
                elif verdict == "REVIEW":
                    review_count += 1
                    print(f"   [?] Frame {frame_idx}: ⚠️ Review (Score: {score:.2f})")
                
                # EARLY STOPPING
                if nsfw_count >= MAX_BAD_FRAMES:
                    print(f"[STOP] Found {MAX_BAD_FRAMES} NSFW frames. Banning.")
                    final_verdict = "NSFW"
                    break 
            
            frame_idx += 1
            
        cap.release()
        
        if final_verdict == "NSFW": return "NSFW"
        if total_frames_checked == 0: return "REVIEW"
        
        # Ratio Logic
        if (nsfw_count / total_frames_checked) > 0.15: return "NSFW"
        if review_count > 2 or nsfw_count > 0: return "REVIEW"
            
        return "SAFE"