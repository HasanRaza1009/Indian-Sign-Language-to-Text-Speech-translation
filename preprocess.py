import cv2
import os
import numpy as np

# Paths
RAW_DATASET = "C:/Users/chakr/OneDrive/Desktop/isl@3/dataset"
PROCESSED_DATASET = "processed_dataset/"
IMG_SIZE = 224

# Create processed dataset folder if not exists
os.makedirs(PROCESSED_DATASET, exist_ok=True)

# Function to apply CLAHE (Adaptive Histogram Equalization) for better contrast
def apply_clahe(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    lab = cv2.merge((l, a, b))
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

# Loop through sign folders
for sign_label in os.listdir(RAW_DATASET):
    input_path = os.path.join(RAW_DATASET, sign_label)
    output_path = os.path.join(PROCESSED_DATASET, sign_label)

    os.makedirs(output_path, exist_ok=True)

    for img_name in os.listdir(input_path):
        img_path = os.path.join(input_path, img_name)

        # Check if it's a valid image file
        try:
            img = cv2.imread(img_path)
            if img is None:
                raise ValueError("Invalid image file")

            # Apply CLAHE for better contrast (optional)
            img = apply_clahe(img)

            # Convert to RGB & Resize
            img_resized = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

            # Normalize pixel values (scale to [0,1] or mean-std normalization)
            img_resized = img_resized.astype(np.float32) / 255.0  # Normalization

            # Convert back to uint8 for saving
            img_resized = (img_resized * 255).astype(np.uint8)

            # Save processed image in standardized format
            processed_img_path = os.path.join(output_path, f"{os.path.splitext(img_name)[0]}.jpg")
            cv2.imwrite(processed_img_path, img_resized)

        except Exception as e:
            print(f"Error processing {img_path}: {e}")
            continue

print("✅ Preprocessing complete! Processed images saved in:", PROCESSED_DATASET)
