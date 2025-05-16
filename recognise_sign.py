# sign_to_speech_translator.py
import cv2
import numpy as np
import tensorflow as tf
import mediapipe as mp
import os
import time

import customtkinter as ctk
from PIL import Image
import tkinter.messagebox as mbox
from gtts import gTTS
from deep_translator import GoogleTranslator
import pygame

# ─── CONFIG ────────────────────────────────────────
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")
pygame.mixer.init()

MODEL_PATH = "C:/Users/chakr/OneDrive/Desktop/isl@3/sign_language_mobilenetv2_finetuned_final.keras"
DATASET_DIR = "C:/Users/chakr/OneDrive/Desktop/isl@3/dataset"
model = tf.keras.models.load_model(MODEL_PATH)
labels = sorted(os.listdir(DATASET_DIR))

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Could not open webcam.")

sign_buffer = []
sentence_buffer = []
capture_start_time = None
recognition_time_threshold = 2
last_prediction = None
last_sign_time = 0
cooldown_time = 1

LANG_OPTIONS = {
    "Hindi": "hi", "French": "fr", "Spanish": "es", "German": "de", "Arabic": "ar", "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW", "Russian": "ru", "Japanese": "ja", "Korean": "ko", "Portuguese": "pt", "Italian": "it",
    "Dutch": "nl", "Turkish": "tr", "Swedish": "sv", "Polish": "pl", "Greek": "el", "Thai": "th", "Vietnamese": "vi",
    "Bengali": "bn", "Tamil": "ta", "Telugu": "te", "Urdu": "ur", "Malayalam": "ml", "Punjabi": "pa", "Marathi": "mr",
    "Gujarati": "gu", "Malay": "ms", "Indonesian": "id", "Hebrew": "he", "Swahili": "sw", "Nepali": "ne", "Sinhala": "si",
    "Kannada": "kn"
}

class SignLangApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🖐 Sign to Speech Translator")
        self.geometry("1200x700")
        self.grid_columnconfigure((0, 1), weight=1, uniform="col")
        self.grid_rowconfigure(0, weight=1)

        def icon(path): return ctk.CTkImage(Image.open(path), size=(20, 20))
        speaker_icon = icon("C:/Users/chakr/Downloads/icons8-speaker-24.png")
        translate_icon = icon("C:/Users/chakr/Downloads/icons8-translate-24.png")
        space_icon = icon("C:/Users/chakr/Downloads/icons8-space-key-24.png")
        back_icon = icon("C:/Users/chakr/Downloads/icons8-back-button-24.png")
        clear_icon = icon("C:/Users/chakr/Downloads/icons8-delete-history-24.png")

        self.video_frame = ctk.CTkFrame(self, corner_radius=16)
        self.video_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.video_frame.grid_rowconfigure(0, weight=1)
        self.video_frame.grid_columnconfigure(0, weight=1)

        self.video_border = ctk.CTkFrame(self.video_frame, corner_radius=10, fg_color="red")
        self.video_border.grid(row=0, column=0, padx=4, pady=4, sticky="nsew")

        self.video_label = ctk.CTkLabel(self.video_border, text="", fg_color="black")
        self.video_label.pack(expand=True, fill="both")

        self.ctrl_frame = ctk.CTkFrame(self, corner_radius=16)
        self.ctrl_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.ctrl_frame.grid_columnconfigure(0, weight=1)

        self.header_label = ctk.CTkLabel(self.ctrl_frame, text="🖐 Sign to Speech Translator", font=("Arial", 22, "bold"))
        self.header_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")

        self.theme_switch = ctk.CTkSwitch(self.ctrl_frame, text="Dark Mode", command=self.toggle_theme)
        self.theme_switch.select()
        self.theme_switch.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="e")

        self.status_label = ctk.CTkLabel(self.ctrl_frame, text="No Hand Detected", text_color=("red", "red"), anchor="w", font=("Arial", 14))
        self.status_label.grid(row=2, column=0, pady=(0, 5), padx=10, sticky="ew")

        self.sentence_label = ctk.CTkLabel(self.ctrl_frame, text="Sentence: ", anchor="w", font=("Arial", 14))
        self.sentence_label.grid(row=3, column=0, padx=10, pady=(0, 0), sticky="ew")

        self.word_label = ctk.CTkLabel(self.ctrl_frame, text="Word: ", anchor="w", font=("Arial", 14))
        self.word_label.grid(row=4, column=0, padx=10, pady=(5, 0), sticky="ew")

        self.sign_label = ctk.CTkLabel(self.ctrl_frame, text="Current Sign: ", anchor="w", font=("Arial", 14))
        self.sign_label.grid(row=5, column=0, padx=10, pady=(5, 10), sticky="ew")

        self.translate_box = ctk.CTkFrame(self.ctrl_frame, corner_radius=12)
        self.translate_box.grid(row=6, column=0, padx=10, pady=10, sticky="ew")
        self.translate_box.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.translate_box, text="Translate to:", font=("Arial", 13)).grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.lang_menu = ctk.CTkOptionMenu(self.translate_box, values=list(LANG_OPTIONS.keys()))
        self.lang_menu.set("Hindi")
        self.lang_menu.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.translated_text = ctk.CTkTextbox(self.translate_box, height=80)
        self.translated_text.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="ew")

        def make_button(text, image, color, command):
            return ctk.CTkButton(self.ctrl_frame, text=text, image=image, fg_color=color, hover_color="#1a1a1a", corner_radius=12, font=("Arial", 14), command=command)

        make_button("Speak", speaker_icon, "green", self.speak_sentence).grid(row=7, column=0, padx=10, pady=5, sticky="ew")
        make_button("Translate", translate_icon, "blue", self.translate_sentence).grid(row=8, column=0, padx=10, pady=5, sticky="ew")
        make_button("Space", space_icon, "blue", self.add_space).grid(row=9, column=0, padx=10, pady=5, sticky="ew")
        make_button("Back", back_icon, "orange", self.backspace).grid(row=10, column=0, padx=10, pady=5, sticky="ew")
        make_button("Clear", clear_icon, "red", self.clear_all).grid(row=11, column=0, padx=10, pady=5, sticky="ew")

        self.after(10, self.update_frame)
        self.bind("<space>", lambda event: self.add_space())
        self.bind("<BackSpace>", lambda event: self.backspace())
        self.bind("<Escape>", lambda event: self.clear_all())

    def toggle_theme(self):
        theme = "Dark" if self.theme_switch.get() else "Light"
        ctk.set_appearance_mode(theme)

    def wait_for_stop(self):
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

    def play_audio(self, filepath):
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
        except Exception as e:
            mbox.showerror("Audio Error", f"Failed to play audio:\n{e}")

    def speak_sentence(self):
        if not sentence_buffer and not sign_buffer:
            return mbox.showwarning("Speak", "No sentence to speak")
        full = sentence_buffer.copy()
        if sign_buffer:
            full.append("".join(sign_buffer))
        s = " ".join(full).strip()
        if not s:
            return mbox.showwarning("Speak", "No content to speak")
        lang = LANG_OPTIONS[self.lang_menu.get()]
        pygame.mixer.music.stop()
        self.wait_for_stop()
        filename = "output.mp3"
        if os.path.exists(filename):
            os.remove(filename)
        tts = gTTS(text=s, lang=lang, slow=False)
        tts.save(filename)
        self.play_audio(filename)

    def translate_sentence(self):
        full = sentence_buffer.copy()
        if sign_buffer:
            full.append("".join(sign_buffer))
        s = " ".join(full).strip()
        if not s:
            return mbox.showwarning("Translate", "Nothing to translate")

        tgt = LANG_OPTIONS[self.lang_menu.get()]
        try:
            out = GoogleTranslator(source="auto", target=tgt).translate(s)
            self.translated_text.delete("0.0", "end")
            self.translated_text.insert("0.0", out)

            pygame.mixer.music.stop()
            self.wait_for_stop()
            filename = "translated_output.mp3"
            if os.path.exists(filename):
                os.remove(filename)
            tts = gTTS(text=out, lang=tgt, slow=False)
            tts.save(filename)
            self.play_audio(filename)

        except Exception as e:
            mbox.showerror("Translate Error", str(e))

    def add_space(self):
        if sign_buffer:
            sentence_buffer.append("".join(sign_buffer))
            sign_buffer.clear()
            self.update_labels()

    def backspace(self):
        if sign_buffer:
            sign_buffer.pop()
            self.update_labels()

    def clear_all(self):
        sign_buffer.clear()
        sentence_buffer.clear()
        self.translated_text.delete("0.0", "end")
        self.update_labels()

    def update_labels(self):
        self.word_label.configure(text=f"Word: {''.join(sign_buffer)}")
        self.sentence_label.configure(text=f"Sentence: {' '.join(sentence_buffer)}")
        self.sign_label.configure(text=f"Current Sign: {sign_buffer[-1] if sign_buffer else ''}")

    def update_frame(self):
        global capture_start_time, last_prediction, last_sign_time
        ret, frame = cap.read()
        if not ret:
            return
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        border_color = "red"
        if results.multi_hand_landmarks:
            border_color = "green"
            self.status_label.configure(text="Hand Detected", text_color=("green", "green"))
            h, w, _ = frame.shape
            xs, ys = [], []
            for handLms in results.multi_hand_landmarks:
                for lm in handLms.landmark:
                    xs.append(int(lm.x * w))
                    ys.append(int(lm.y * h))
                mp_drawing.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
            if xs and ys:
                x1, x2 = max(min(xs) - 40, 0), min(max(xs) + 40, w)
                y1, y2 = max(min(ys) - 40, 0), min(max(ys) + 40, h)
                roi = frame[y1:y2, x1:x2]
                if roi.size:
                    roi = cv2.resize(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB), (160, 160)) / 255.0
                    pred = model.predict(np.expand_dims(roi, 0), verbose=0)
                    lbl = labels[np.argmax(pred)]
                    now = time.time()
                    if lbl == last_prediction:
                        if capture_start_time is None:
                            capture_start_time = now
                        elif now - capture_start_time >= recognition_time_threshold:
                            if now - last_sign_time > cooldown_time:
                                sign_buffer.append(lbl)
                                last_sign_time = now
                            capture_start_time = None
                    else:
                        capture_start_time = None
                    last_prediction = lbl
                    self.update_labels()
        else:
            self.status_label.configure(text="No Hand Detected", text_color=("red", "red"))
            capture_start_time = None

        img = Image.fromarray(img_rgb)
        ctk_img = ctk.CTkImage(img, size=(640, 480))
        self.video_label.configure(image=ctk_img)
        self.video_label.image = ctk_img
        self.video_border.configure(fg_color=border_color)
        self.after(10, self.update_frame)

if __name__ == "__main__":
    app = SignLangApp()
    app.mainloop()
    cap.release()
