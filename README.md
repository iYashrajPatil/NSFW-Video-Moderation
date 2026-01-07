---
title: NSFW Video & Multi-Modal Moderator
emoji: 🛡️
colorFrom: blue
colorTo: red
sdk: docker
pinned: false
app_port: 7860
---

# 🛡️ Multi-Modal NSFW Video Moderation API

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-High%20Performance-green?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)

**A high-speed, privacy-first moderation system powered by Vision Transformers (ViT) & Audio Analysis.**

[View Live Demo](https://huggingface.co/spaces/Yashrajp12/NSFW-Video-Moderator) · [Report Bug](https://github.com/Yashrajp12/NSFW-Video-Moderation/issues)

</div>

---

## 📖 About The Project

This is a robust open-source API designed to detect explicit (NSFW) content in user-uploaded videos. 

Unlike traditional frame-scanners, this system employs a **Multi-Modal approach**. It doesn't just "watch" the video; it "listens" to it. By combining **Vision Transformers (ViT)** for visual frames and **Audio Analysis** for spoken context, it drastically reduces false positives and detects inappropriate content that visual-only models might miss.

### ✨ Key Features

* **🎥 Multi-Modal Analysis:** Cross-references visual data with audio transcripts to ensure high-accuracy detection.
* **⚡ Blazing Fast:** Intelligently samples frames (e.g., 1 frame every 1.5s) and resizes for rapid inference without losing context.
* **🧠 Context Aware:** Detects "NSFW context" (lingerie, suggestive poses) and inappropriate language simultaneously.
* **🔒 Privacy Focused:** Runs entirely on your own infrastructure (Local or Cloud). No video data is ever sent to third-party APIs.
* **🐳 Docker Ready:** Fully containerized for one-click deployment to Hugging Face Spaces or Render.

---

## 🛠️ Technology Stack

* **Core:** Python 3.10
* **API Framework:** FastAPI + Uvicorn
* **Computer Vision:** OpenCV (`cv2`) & Vision Transformers
* **Audio Processing:** MoviePy (Audio Extraction) & Speech Recognition
* **Deployment:** Docker

---

## 🚀 Getting Started (Local)

Follow these steps to get the API running on your local machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/Yashrajp12/NSFW-Video-Moderation.git](https://github.com/Yashrajp12/NSFW-Video-Moderation.git)
cd "NSFW VIDEO MODERATION"
```
### 2. Install Dependencies
```Bash
pip install -r requirements.txt
```
### 3. Run the Server
```Bash
python server.py
```
###### Note: The first launch will automatically download the necessary AI models. Please allow it a moment to complete.

### 4. Test the API
Open your browser to the interactive Swagger UI:

👉 http://localhost:7860/docs

## ☁️ Deployment (Hugging Face Spaces)
This project is optimized for the Hugging Face Free Tier using the Docker SDK.

### Option A: Push via Git (Recommended)
If you have already created a Space with the Docker SDK:

```Bash

# Add your Space as a remote
git remote add space [https://huggingface.co/spaces/Yashrajp12/NSFW-Video-Moderator](https://huggingface.co/spaces/Yashrajp12/NSFW-Video-Moderator)

# Push your code
git push space main
```
### Option B: Manual Setup
1. Create a new Space on Hugging Face.

2. Select Docker as the SDK.

3. Go to Settings > Git Repository and link this GitHub repo.

## 🔌 API Reference

POST /moderate
Upload a video file to receive a detailed moderation verdict.

Request: multipart/form-data

- file: (Video File) .mp4, .avi, .mov

Response (JSON):
```bash

JSON

{
  "verdict": "UNSAFE",
  "confidence_score": 0.98,
  "details": {
    "visual_flag": true,
    "audio_flag": false,
    "nsfw_frame_count": 3
  },
  "process_time_seconds": 2.45
}
```
## 📂 Project Structure
```text

NSFW VIDEO MODERATION/
├── Dockerfile          # 🐳 Configuration for cloud deployment
├── README.md           # 📄 Documentation
├── moderator.py        # 🧠 Core Multi-Modal logic (ViT + Audio)
├── requirements.txt    # 📦 Python dependencies
└── server.py           # 🚀 Entry point for the FastAPI server
```
## 🤝 Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

1. Fork the Project

2. Create your Feature Branch (git checkout -b feature/AmazingFeature)

3. Commit your Changes (git commit -m 'Add some AmazingFeature')

4. Push to the Branch (git push origin feature/AmazingFeature)

5. Open a Pull Request

## 📄 License
Distributed under the MIT License. See LICENSE for more information.

<div align="center"> <br /> Made with ❤️ by <a href="https://www.google.com/search?q=https://github.com/Yashrajp12">Yashraj Patil</a> </div>