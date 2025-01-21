from flask import Flask, request, jsonify
import cv2
import numpy as np
import time
import torch

app = Flask(__name__)
url = input("Server URL Giriniz: ") 


def load_model():
    print("Model yükleniyor...")
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s').to(device)
    print("Model başarıyla yüklendi.")
    return model


model = load_model()

@app.route('/process-video', methods=['POST'])
def process_video():
    start_time = time.perf_counter()

    # Fotoğrafı al
    if 'frame' not in request.files:
        return jsonify({"error": "No frame provided"}), 400

    file = request.files['frame']
    frame_data = file.read()

    np_frame = np.frombuffer(frame_data, dtype=np.uint8)
    frame = cv2.imdecode(np_frame, cv2.IMREAD_COLOR)

    if frame is None:
        return jsonify({"error": "Failed to decode frame"}), 400

    
    try:
        results = model(frame)
        detections = results.pred[0].cpu().numpy()  # Tahminleri CPU'ya taşı ve NumPy array'e dönüştür
        people_count = len([x for x in detections if int(x[5]) == 0])  # Class 0: 'person'
    except Exception as e:
        return jsonify({"error": f"Model error: {str(e)}"}), 500

    latency = time.perf_counter() - start_time  

    
    return jsonify({"people_count": people_count, "latency": latency}), 200

if __name__ == '__main__':
    print("Server başlatılıyor...")
    app.run(host=url, port=80)  # server url