# text_moderator.py
from transformers import pipeline
import logging

class TextModerator:
    def __init__(self):
        print("[INFO] Loading Text Model...")
        # running on CPU usually fits better for text to save GPU for video
        self.pipe = pipeline("text-classification", model="unitary/toxic-bert", top_k=None)

    def predict(self, text):
        """
        Returns: SAFE, REVIEW, or NSFW
        """
        if not text or len(text.strip()) == 0:
            return "SAFE"

        results = self.pipe(text)[0]
        
        # We check the top scores
        severe_toxic = 0.0
        mild_toxic = 0.0

        for label in results:
            score = label['score']
            name = label['label']
            
            # High severity categories
            if name in ['severe_toxic', 'identity_hate', 'threat', 'insult'] and score > 0.7:
                return "NSFW"
            
            # Accumulate mild toxicity
            if name in ['toxic', 'obscene']:
                mild_toxic += score

        if mild_toxic > 0.6:
            return "REVIEW"
            
        return "SAFE"