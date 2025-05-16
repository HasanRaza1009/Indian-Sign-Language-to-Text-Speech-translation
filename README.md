# Indian-Sign-Language-to-Text/Speech-translation

An AI-powered system that translates Indian Sign Language (ISL) gestures captured from a webcam into real-time text and speech. This project bridges the communication gap between the hearing and speech-impaired communities and the rest of the world.

---

## 🚀 Project Overview

This project uses computer vision and deep learning (CNN - MobileNetV2) to recognize hand gestures from Indian Sign Language (ISL) in real-time. It converts these gestures to text and then to speech using gTTS (Google Text-to-Speech). The system provides a user-friendly GUI built with Tkinter and supports multilingual translation.

---

## 📌 Features

- Real-time gesture recognition using MediaPipe  
- Deep learning model (MobileNetV2) for classification  
- Text-to-speech output using gTTS  
- Multilingual support with language selection  
- CLAHE-based image preprocessing for better model accuracy  
- User-friendly GUI interface using Tkinter  
- Organized module-based project structure  

---

## 🧱 Project Structure

```
Indian-Sign-Language-to-Text-Speech-translation/
├── capture.py               # GUI to capture gesture images using webcam
├── preprocess.py            # Preprocess captured images with CLAHE
├── model.py                 # Train MobileNetV2 CNN on processed data
├── recognise_sign.py        # Real-time translator: Sign → Text → Speech
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── model/                   # Saved trained model files
├── dataset/                 # Captured and preprocessed gesture images
│   ├── A/
│   ├── B/
│   └── ...
└── assets/                  # UI icons, reference images, etc.
```

---

## 🛠️ Installation

### 1. Clone the repository:

```bash
git clone https://github.com/HasanRaza1009/Indian-Sign-Language-to-Text-Speech-translation.git
cd Indian-Sign-Language-to-Text-Speech-translation
```

### 2. Create and activate a virtual environment (recommended):

```bash
python -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install required packages:

```bash
pip install -r requirements.txt
```

> ⚠️ Python version must be between 3.8 and 3.10 for compatibility.

---

## 📦 Requirements

- Python 3.8 - 3.10  
- Webcam  
- Stable internet connection (needed for Google Text-to-Speech)  
- Packages listed in `requirements.txt`, including but not limited to:  
  - tensorflow==2.12.0  
  - opencv-python==4.7.0.72  
  - mediapipe==0.10.3  
  - numpy==1.24.3  
  - Pillow==9.5.0  
  - gTTS==2.3.2  
  - scikit-learn==1.2.2  
  - matplotlib==3.7.1  

> Tkinter comes pre-installed with Python.

---

## 📸 Usage

### Step 1: Capture dataset images

```bash
python capture.py
```

- Use the GUI to record gesture images (alphabets, digits) through your webcam.

### Step 2: Preprocess dataset

```bash
python preprocess.py
```

- Applies CLAHE for contrast enhancement and resizes images to prepare for training.

### Step 3: Train the model

```bash
python model.py
```

- Trains MobileNetV2 CNN on your preprocessed images and saves the trained model.

### Step 4: Run real-time sign language translator

```bash
python recognise_sign.py
```

- Opens webcam and translates recognized ISL signs to text and speech in real-time.

---

## 🌐 Multilingual Support

- Select your preferred language in the GUI before running the translator.  
- Uses Google Text-to-Speech (gTTS) API to speak recognized text in the selected language (e.g., Hindi, Kannada, etc.).

---

## ✍️ Contributing

Contributions are welcome! To contribute:

- Fork the repo  
- Create a new branch:  
  ```bash
  git checkout -b feature/YourFeature
  ```
- Commit your changes:  
  ```bash
  git commit -m "Add YourFeature"
  ```
- Push the branch:  
  ```bash
  git push origin feature/YourFeature
  ```
- Open a Pull Request for review.

---

## 💡 Future Enhancements

- Sentence prediction and grouping words for natural language output  
- Support for dynamic gesture recognition (moving signs)  
- Deployment as a mobile or web app for wider accessibility

---

## 📄 License

This project is licensed under the MIT License.

---

Thank you for checking out this project!  
Feel free to open issues or reach out with questions.
