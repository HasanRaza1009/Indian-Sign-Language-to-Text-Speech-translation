# Indian-Sign-Language-to-Text/Speech-translation
An AI-powered system that translates Indian Sign Language (ISL) gestures captured from a webcam into real-time text and speech. This project bridges the communication gap between the hearing and speech-impaired communities and the rest of the world.

🚀 Project Overview
This project uses computer vision and deep learning (CNN - MobileNetV2) to recognize hand gestures from Indian Sign Language (ISL) in real-time. It converts these gestures to text and then to speech using gTTS (Google Text-to-Speech). The system provides a user-friendly GUI built with Tkinter and supports multilingual translation.

📌 Features
🔍 Real-time gesture recognition using MediaPipe
🤖 Deep learning model (MobileNetV2) for classification
🗣️ Text-to-speech output using gTTS
🌐 Multilingual support with language selection
🖼️ CLAHE-based image preprocessing for better model accuracy
🖥️ User-friendly GUI interface using Tkinter
📁 Organized module-based structure

🧱 Project Structure
ISL-Translator/
├── capture.py               # GUI to capture gesture images using webcam
├── preprocess.py            # Preprocess captured images using CLAHE
├── model.py                 # Trains CNN (MobileNetV2) on preprocessed data
├── recognise_sign.py        # Real-time translator: Sign → Text → Speech
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── model/                   # Trained MobileNetV2 model
├── dataset/                 # Captured and preprocessed images
│   ├── A/
│   ├── B/
│   ├── ...
└── assets/                  # UI icons, reference images, etc.


🛠️ Installation
Clone the repository:
git clone https://github.com/HasanRaza1009/Indian-Sign-Language-to-Text-Speech-translation.git
cd Indian-Sign-Language-to-Text-Speech-translation

Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt
Make sure your Python version is 3.8 to 3.10.

📦 Requirements
Python 3.8–3.10
Webcam
Stable internet connection (for gTTS)
Installed packages (from requirements.txt):
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
Step-by-step:
📷 Capture Dataset:
python capture.py
Use the GUI to record gesture images of alphabets and digits using your webcam.

🎨 Preprocess the Dataset:
python preprocess.py
Applies CLAHE and resizes images for training.

🧠 Train the Model:
python model.py
This uses a transfer learning MobileNetV2 CNN model and saves the trained weights.

🤖 Run the Real-Time Translator:
python recognise_sign.py
The application will open your webcam, recognize the sign, display the text, and convert it to speech.

🗣️ Multilingual Support
The system uses gTTS and supports translation to multiple languages (e.g., Hindi, Kannada, etc.). You can select the target language in the GUI before starting translation.

✍️ Contributing
Contributions are welcome! Feel free to fork the repo and submit pull requests.
Fork the repository
Create your feature branch: git checkout -b feature/YourFeature
Commit your changes: git commit -m 'Add YourFeature'
Push to the branch: git push origin feature/YourFeature
Open a pull request

💡 Future Work
Add sentence prediction and word grouping
Include dynamic gesture recognition (currently static)
Deploy as a mobile app or web-based solution
