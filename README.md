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

- Indian-Sign-Language-to-Text-Speech-translation/
- ├── capture.py # GUI to capture gesture images using webcam
- ├── preprocess.py # Preprocess captured images using CLAHE
- ├── model.py # Trains MobileNetV2 CNN model on preprocessed data
- ├── recognise_sign.py # Real-time translator: Sign → Text → Speech
- ├── requirements.txt # Python dependencies
- ├── README.md # Project documentation
- ├── model/ # Trained MobileNetV2 model
- ├── dataset/ # Captured and preprocessed images
- │ ├── A/
- │ ├── B/
- │ └── ...
- └── assets/ # UI icons, reference images, etc.

---

## 🛠️ Installation

### 1. Clone the Repository


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
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
📌 Ensure your Python version is between 3.8 and 3.10.

📦 Requirements
Python 3.8–3.10

Webcam

Stable Internet connection (for gTTS API)

Installed Python packages:

ini
Copy
Edit
tensorflow==2.12.0  
opencv-python==4.7.0.72  
mediapipe==0.10.3  
numpy==1.24.3  
Pillow==9.5.0  
gTTS==2.3.2  
scikit-learn==1.2.2  
matplotlib==3.7.1  
Tkinter comes pre-installed with Python.

📸 Usage
1. Capture Dataset
bash
Copy
Edit
python capture.py
Use the GUI to record gesture images (alphabets/digits) using your webcam.

2. Preprocess the Dataset
bash
Copy
Edit
python preprocess.py
This applies CLAHE for contrast enhancement and resizes images for CNN training.

3. Train the Model
bash
Copy
Edit
python model.py
Trains the MobileNetV2 model on preprocessed images and saves it in the model/ directory.

4. Run the Real-Time Translator
bash
Copy
Edit
python recognise_sign.py
Launches the webcam app to recognize gestures in real time and speak the translated text.

🌍 Multilingual Support
You can select your desired language in the GUI before running translation. The system uses gTTS to convert recognized text to speech in the selected language (e.g., Hindi, Kannada).

✍️ Contributing
We welcome contributions! Here’s how you can contribute:

Fork the repository

Create a new branch:

bash
Copy
Edit
git checkout -b feature/YourFeature
Commit your changes:

bash
Copy
Edit
git commit -m "Add YourFeature"
Push to your branch:

bash
Copy
Edit
git push origin feature/YourFeature
Open a pull request 🚀

💡 Future Work
Add sentence prediction and word grouping from continuous gestures

Recognize dynamic (moving) sign gestures

Deploy the solution as a mobile or web application
