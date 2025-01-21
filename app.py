import cv2
import requests

url = input("Server URL Giriniz: ") 

gst_pipeline="libcamerasrc ! video/x-raw ! videoconvert ! appsink"
cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
if not cap.isOpened():
    print("Kamera açılamadı!")
    exit()

while True:
    ret, frame = cap.read() 
    if not ret:
        print("Kamera görüntüsü alınamadı.")
        break

    
    _, img_encoded = cv2.imencode('.jpg', frame)

    
    files = {'frame': ('frame.jpg', img_encoded.tobytes())}
    try:
        response = requests.post(url, files=files, timeout=5)
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Detected people: {data['people_count']}, Latency: {data['latency']} seconds")
            except ValueError:
                print("Response is not in JSON format.")
                print(f"Raw response: {response.text}")
        else:
            print(f"Error: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Bağlantı hatası: {e}")

   
  

cap.release() 
cv2.destroyAllWindows()