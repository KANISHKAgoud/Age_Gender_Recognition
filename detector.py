import cv2
from PIL import Image
from transformers import pipeline

# OpenCV built-in face detector
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Standard public models (no custom task required)
gender_classifier = pipeline(
    "image-classification",
    model="dima806/fairface_gender_image_detection"
)

age_classifier = pipeline(
    "image-classification",
    model="nateraw/vit-age-classifier"
)


def detect_face_and_predict(frame):
    results = []

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]

        if face.size == 0:
            continue

        face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(face_rgb)

        # Predict gender
        gender_pred = gender_classifier(pil_img)[0]["label"]

        # Predict age range
        age_pred = age_classifier(pil_img)[0]["label"]

        results.append({
            "box": [int(x), int(y), int(w), int(h)],
            "gender": str(gender_pred),
            "age": str(age_pred)
        })

    return results