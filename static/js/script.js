const imageBtn = document.getElementById("imageBtn");
const webcamBtn = document.getElementById("webcamBtn");
const captureBtn = document.getElementById("captureBtn");
const imageInput = document.getElementById("imageInput");

const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const resultBox = document.getElementById("resultBox");

let webcamStream = null;

function drawImageToCanvas(img) {
  canvas.width = img.width;
  canvas.height = img.height;
  ctx.drawImage(img, 0, 0);
}

function drawPredictions(results) {
  if (!results.length) {
    resultBox.innerHTML = "No face detected.";
    return;
  }

  let html = "";

  results.forEach((item, index) => {
    const [x, y, w, h] = item.box;

    ctx.strokeStyle = "#22c55e";
    ctx.lineWidth = 3;
    ctx.strokeRect(x, y, w, h);

    ctx.fillStyle = "#22c55e";
    ctx.fillRect(x, y - 30, w, 30);

    ctx.fillStyle = "#000";
    ctx.font = "16px Arial";
    ctx.fillText(`${item.gender}, ${item.age}`, x + 8, y - 10);

    html += `<div>Face ${index + 1}: <strong>${item.gender}</strong>, ${item.age}</div>`;
  });

  resultBox.innerHTML = html;
}

imageBtn.addEventListener("click", () => imageInput.click());

imageInput.addEventListener("change", async (e) => {
  const file = e.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("image", file);

  const img = new Image();
  img.src = URL.createObjectURL(file);
  img.onload = () => drawImageToCanvas(img);

  resultBox.innerHTML = "Processing image...";

  const res = await fetch("/predict-image", {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  drawPredictions(data.results || []);
});

webcamBtn.addEventListener("click", async () => {
  webcamStream = await navigator.mediaDevices.getUserMedia({ video: true });

  video.srcObject = webcamStream;
  video.hidden = false;
  captureBtn.hidden = false;

  video.onloadedmetadata = () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0);
  };

  resultBox.innerHTML = "Webcam started. Capture a frame.";
});

captureBtn.addEventListener("click", async () => {
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  canvas.toBlob(async (blob) => {
    const formData = new FormData();
    formData.append("frame", blob, "webcam.jpg");

    resultBox.innerHTML = "Processing webcam frame...";

    const res = await fetch("/predict-webcam", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    drawPredictions(data.results || []);
  }, "image/jpeg");
});