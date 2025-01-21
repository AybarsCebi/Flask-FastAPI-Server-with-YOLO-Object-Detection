This project implements a Flask or FastAPI server with a REST API to handle video streaming and real-time object detection using YOLO and Tiny YOLO models.

Part 1: Video Streaming and People Counting

Device: Captures video and sends it to the server.

Server:
Applies YOLO (You Only Look Once) object detection on the received frames.
Streams the number of people detected in each frame back to the client.

Part 2: Tiny YOLO Object Detection and Bounding Box Streaming

Device:
Captures video and applies Tiny YOLO for object detection.
Sends the list of detected objects (bounding boxes and classes) to the server.
Streams the original image with bounding boxes overlaid.

Server:
Streams the number of detected people to the client.

Performance Metric:
The system computes and tracks latency, which is the time difference between:
When the image is captured on the device.
When the number of people is counted on the server.
