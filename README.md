# 🛡️ AI-Powered NSFW Video Moderation API

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-High%20Performance-green?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

**A high-speed, privacy-first video moderation system powered by Vision Transformers (ViT).**

[Report Bug](https://github.com/iYashrajPatil/NSFW-Video-Moderation/issues) · [Request Feature](https://github.com/iYashrajPatil/NSFW-Video-Moderation/issues)

</div>

---

## 📖 About The Project

This is a robust open-source API designed to detect explicit (NSFW) content in user-uploaded videos. Unlike traditional frame-by-frame scanners that are slow and costly, this system uses an **intelligent sampling engine** combined with a **Vision Transformer (ViT)** model (`Falconsai/nsfw_image_detection`).

### ✨ Key Features

* **⚡ Blazing Fast:** Intelligently samples frames (e.g., 1 frame every 1.5s) and resizes to 224x224 for rapid inference.
* **🧠 Context Aware:** Detects "NSFW context" (lingerie, suggestive poses, skin ratio) effectively, even without explicit nudity.
* **🔒 Privacy Focused:** Runs entirely on your own infrastructure (Local or Cloud). No video data is ever sent to third-party APIs.
* **🐳 Docker Ready:** Comes with a pre-configured `Dockerfile` for one-click deployment to Hugging Face Spaces or Render.

---

## 🛠️ Technology Stack

* **Core:** Python 3.10
* **API Framework:** FastAPI + Uvicorn
* **Computer Vision:** OpenCV (`cv2`) & Pillow (`PIL`)
* **AI Model:** Hugging Face Transformers & PyTorch

---

## 🚀 Getting Started (Local)

Follow these steps to get the API running on your local machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/iYashrajPatil/NSFW-Video-Moderation.git](https://github.com/iYashrajPatil/NSFW-Video-Moderation.git)
cd NSFW-Video-Moderation
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Run the Server
```bash
python server.py
```
##### Note: The first launch will automatically download the AI model (~300MB). Please allow it a moment to complete.

### 4. Test the API
Open your browser to the interactive Swagger UI: 👉 http://localhost:8000/docs

## ☁️ Deployment (Hugging Face Spaces)
This project is optimized for the Hugging Face Free Tier using the Docker SDK.

### Option A: Push via Git (Recommended)
If you have already created a Space with the Docker SDK:
```bash
# Add your Space as a remote
git remote add space [https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME](https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME)

# Push your code
git push space main
```
### Option B: Manual Setup
Create a new Space on Hugging Face.

Select Docker as the SDK.

Go to Settings > Git Repository and link this GitHub repo.

## 🔌 API Reference
POST /check_video
Upload a video file to receive a moderation verdict.

Request: multipart/form-data

- file: (Video File) .mp4, .avi, .mov
```bash
{
  "verdict": "UNSAFE",
  "processed_frames": 12,
  "nsfw_frame_count": 3,
  "process_time_seconds": 2.45,
  "flagged_segments": [
    {
      "timestamp": 4.5,
      "score": 0.98,
      "label": "NSFW"
    }
  ]
}
```
## 📂 Project Structure
NSFW-Video-Moderation/
├── server.py           # 🚀 Entry point for the FastAPI server
├── moderator.py        # 🧠 Core logic (ViT Model + OpenCV sampling)
├── requirements.txt    # 📦 Python dependencies
├── Dockerfile          # 🐳 Configuration for cloud deployment
└── README.md           # 📄 Documentation

## 🤝 Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

1. Fork the Project

2. Create your Feature Branch (git checkout -b feature/AmazingFeature)

3. Commit your Changes (git commit -m 'Add some AmazingFeature')

4. Push to the Branch (git push origin feature/AmazingFeature)

5. Open a Pull Request

## 📄 License
Distributed under the MIT License. See LICENSE for more information.

<div align="center"> <br /> Made with ❤️ by <a href="https://www.google.com/search?q=https://github.com/iYashrajPatil">Yashraj Patil</a> </div>