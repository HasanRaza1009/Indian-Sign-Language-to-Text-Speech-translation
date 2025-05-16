# 🤟 Indian Sign Language to Text/Speech Translation

An AI-powered system that translates Indian Sign Language (ISL) gestures captured from a webcam into real-time text and speech. This project bridges the communication gap between the hearing and speech-impaired communities and the rest of the world.

---

## 🚀 Project Overview

This project leverages computer vision and deep learning (MobileNetV2 CNN) to recognize hand gestures from Indian Sign Language (ISL) in real-time. It converts recognized gestures to text, then to speech using Google Text-to-Speech (gTTS), and supports multilingual output via a Tkinter-based GUI.

---

## 📌 Features

- 🔍 Real-time gesture recognition using MediaPipe
- 🤖 Deep learning-based classification using MobileNetV2
- 🗣️ Text-to-speech conversion using gTTS
- 🌐 Multilingual support (e.g., Hindi, Kannada, etc.)
- 🎨 CLAHE-based image preprocessing for contrast enhancement
- 🖥️ User-friendly GUI built using Tkinter
- 📁 Well-organized modular structure

---

## 🧱 Project Structure
Indian-Sign-Language-to-Text-Speech-translation/
├── capture.py # GUI to capture gesture images using webcam
├── preprocess.py # Preprocess captured images using CLAHE
├── model.py # Trains MobileNetV2 CNN model on preprocessed data
├── recognise_sign.py # Real-time translator: Sign → Text → Speech
├── requirements.txt # Python dependencies
├── README.md # Project documentation
├── model/ # Trained MobileNetV2 model
├── dataset/ # Captured and preprocessed images
│ ├── A/
│ ├── B/
│ └── ...
└── assets/ # UI icons, reference images, etc.

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/HasanRaza1009/Indian-Sign-Language-to-Text-Speech-translation.git
cd Indian-Sign-Language-to-Text-Speech-translation

2. Create a Virtual Environment (optional but recommended)
bash
Copy
Edit
python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
