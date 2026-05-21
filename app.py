import os
import cv2
from flask import Flask, render_template, request, jsonify
from detector import detect_face_and_predict

app = Flask(__name__)

# Disable caching (VERY IMPORTANT for development)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict-image", methods=["POST"])
def predict_image():
    file = request.files.get("image")

    if not file:
        return jsonify({"error": "No image uploaded"}), 400

    path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(path)

    frame = cv2.imread(path)
    if frame is None:
        return jsonify({"error": "Invalid image"}), 400

    results = detect_face_and_predict(frame)
    return jsonify({"results": results, "image": path})


@app.route("/predict-webcam", methods=["POST"])
def predict_webcam():
    file = request.files.get("frame")

    if not file:
        return jsonify({"error": "No frame received"}), 400

    path = os.path.join(app.config["UPLOAD_FOLDER"], "webcam.jpg")
    file.save(path)

    frame = cv2.imread(path)
    if frame is None:
        return jsonify({"error": "Invalid frame"}), 400

    results = detect_face_and_predict(frame)
    return jsonify({"results": results})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)