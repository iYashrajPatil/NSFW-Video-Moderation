# image_moderator.py
import torch
from transformers import AutoModelForImageClassification, ViTImageProcessor, CLIPProcessor, CLIPModel

# --- FIX: Removed the circular import line that was here ---

class ImageModerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[INFO] Loading Visual Models on {self.device}...")

        # 1. Fast Nudity Detector (Falconsai)
        self.nsfw_model_name = "Falconsai/nsfw_image_detection"
        # use_fast=True silences warnings
        self.nsfw_processor = ViTImageProcessor.from_pretrained(self.nsfw_model_name, use_fast=True)
        self.nsfw_model = AutoModelForImageClassification.from_pretrained(self.nsfw_model_name).to(self.device)

        # 2. Context Brain (CLIP)
        self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device)
        self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

        self.context_labels = [
            "woman in traditional saree",   # Index 0
            "woman in gym fitness wear",    # Index 1
            "lingerie or nudity",           # Index 2
            "sexually suggestive pose"      # Index 3
        ]

    def predict(self, pil_image):
        # 1. Fast Check
        inputs = self.nsfw_processor(images=pil_image, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.nsfw_model(**inputs)
            probs = outputs.logits.softmax(dim=1)
        
        nsfw_score = probs[0][1].item()
        
        if nsfw_score < 0.15: return "SAFE", nsfw_score
        if nsfw_score > 0.85: return "NSFW", nsfw_score

        # 2. Context Check (CLIP)
        inputs = self.clip_processor(
            text=self.context_labels, images=pil_image, return_tensors="pt", padding=True
        ).to(self.device)

        with torch.no_grad():
            outputs = self.clip_model(**inputs)
            probs = outputs.logits_per_image.softmax(dim=1)[0]

        best_idx = probs.argmax().item()
        confidence = probs[best_idx].item()

        if best_idx == 0 and confidence > 0.6: return "SAFE", nsfw_score
        if best_idx == 1 and confidence > 0.7: return "SAFE", nsfw_score
        if best_idx == 3 and confidence > 0.8: return "REVIEW", nsfw_score

        return "REVIEW", nsfw_score