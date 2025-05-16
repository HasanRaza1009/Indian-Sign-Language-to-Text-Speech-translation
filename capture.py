import cv2
import os
import mediapipe as mp
import threading
import time
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

# ----------------- Initialize MediaPipe ------------------
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)

# ----------------- Create Dataset Directory ------------------
dataset_root = "dataset"
os.makedirs(dataset_root, exist_ok=True)

# ----------------- Globals ------------------
cap = cv2.VideoCapture(0)
max_images = 4000
capturing = False
stop_requested = False
sign_label = ""
img_count = 0
video_label = None
count_label = None
start_button = None
stop_button = None
preview_label = None
progress_bar = None
preview_window = None
preview_image_label = None

# ----------------- Update Video Frame ------------------
def update_frame():
    global cap, video_label
    ret, frame = cap.read()
    if not ret or frame is None:
        return
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    if not capturing:
        root.after(10, update_frame)

# ----------------- Update Live Cropped Hand Preview ------------------
def update_preview_window(image):
    global preview_window, preview_image_label
    if preview_window is None:
        preview_window = Toplevel(root)
        preview_window.title("Live Hand Preview")
        preview_image_label = Label(preview_window)
        preview_image_label.pack()
        preview_window.geometry("180x180")

    img = image.resize((160, 160))
    imgtk = ImageTk.PhotoImage(image=img)
    preview_image_label.config(image=imgtk)
    preview_image_label.image = imgtk

# ----------------- Capture Images in Thread ------------------
def capture_images():
    global cap, sign_label, img_count, capturing, max_images, count_label, stop_requested, preview_label, progress_bar
    capturing = True
    stop_requested = False

    sign_folder = os.path.join(dataset_root, sign_label)
    os.makedirs(sign_folder, exist_ok=True)
    img_count = len(os.listdir(sign_folder))

    count_label.config(text="Get ready! Starting in 5 seconds...")
    time.sleep(5)

    while img_count < max_images and not stop_requested:
        ret, frame = cap.read()
        if not ret or frame is None:
            continue

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        h, w, _ = frame.shape
        x_min, y_min, x_max, y_max = w, h, 0, 0

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for lm in hand_landmarks.landmark:
                    x, y = int(lm.x * w), int(lm.y * h)
                    x_min, y_min = min(x, x_min), min(y, y_min)
                    x_max, y_max = max(x, x_max), max(y, y_max)

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Add padding
            padding = 40
            x_min, y_min = max(0, x_min - padding), max(0, y_min - padding)
            x_max, y_max = min(w, x_max + padding), min(h, y_max + padding)
            hand_roi = frame[y_min:y_max, x_min:x_max]

            if hand_roi.size != 0:
                # Preview captured hand
                hand_rgb = cv2.cvtColor(hand_roi, cv2.COLOR_BGR2RGB)
                hand_img = Image.fromarray(hand_rgb)

                # Show in main preview
                hand_img_resized = hand_img.resize((160, 160))
                hand_imgtk = ImageTk.PhotoImage(image=hand_img_resized)
                preview_label.config(image=hand_imgtk, text="")
                preview_label.image = hand_imgtk

                # Show in external live window
                update_preview_window(hand_img)

                # Save to file
                img_filename = os.path.join(sign_folder, f"{sign_label}_{img_count + 1}.jpg")
                cv2.imwrite(img_filename, hand_roi)
                img_count += 1

                # Update UI
                count_label.config(text=f"Image {img_count} of {max_images}")
                progress_bar["value"] = img_count
                progress_bar.update()

        update_frame()

    capturing = False
    start_button.config(state=NORMAL)
    stop_button.config(state=DISABLED)

    if stop_requested:
        count_label.config(text=f"Capture stopped at {img_count} images.")
    else:
        messagebox.showinfo("Done", f"Captured {img_count} images for '{sign_label}'")

# ----------------- Start Capture Button ------------------
def start_capture():
    global sign_label, start_button, stop_button, progress_bar
    lbl = entry.get().strip().lower()

    if not lbl.isalnum() or len(lbl) != 1:
        messagebox.showerror("Invalid Input", "Enter a single character (A-Z or 1-9).")
        return

    sign_label = lbl
    start_button.config(state=DISABLED)
    stop_button.config(state=NORMAL)
    progress_bar["value"] = 0
    progress_bar["maximum"] = max_images
    count_label.config(text="Preparing to capture...")
    threading.Thread(target=capture_images).start()

# ----------------- Stop Capture Button ------------------
def stop_capture():
    global stop_requested
    stop_requested = True

# ----------------- Exit ------------------
def on_closing():
    global cap
    cap.release()
    cv2.destroyAllWindows()
    root.destroy()

# ----------------- GUI ------------------
root = Tk()
root.title("Sign Language Image Capture")
root.geometry("800x750")
root.configure(bg="#2b2b2b")

title = Label(root, text="Sign Language Dataset Capture Tool", font=("Helvetica", 20, "bold"), fg="white", bg="#2b2b2b")
title.pack(pady=10)

video_label = Label(root, bg="black", width=640, height=480)
video_label.pack(pady=10)

frame_controls = Frame(root, bg="#2b2b2b")
frame_controls.pack(pady=5)

Label(frame_controls, text="Enter Sign (A-Z or 1-9): ", font=("Helvetica", 14), bg="#2b2b2b", fg="white").grid(row=0, column=0, padx=5)
entry = Entry(frame_controls, font=("Helvetica", 14), width=5, justify='center')
entry.grid(row=0, column=1, padx=5)

start_button = Button(frame_controls, text="Start Capture", command=start_capture, font=("Helvetica", 14), bg="#4CAF50", fg="white", padx=10)
start_button.grid(row=0, column=2, padx=10)

stop_button = Button(frame_controls, text="Stop", command=stop_capture, font=("Helvetica", 14), bg="#ff9800", fg="white", padx=10, state=DISABLED)
stop_button.grid(row=0, column=3, padx=10)

count_label = Label(root, text="", font=("Helvetica", 14), fg="yellow", bg="#2b2b2b")
count_label.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=500, mode='determinate')
progress_bar.pack(pady=5)

preview_label = Label(root, text="Preview will appear here", bg="#2b2b2b", fg="white")
preview_label.pack(pady=10)

Button(root, text="Exit", command=on_closing, font=("Helvetica", 14), bg="#f44336", fg="white", padx=20).pack(pady=10)

update_frame()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
