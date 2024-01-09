from ultralytics import YOLO
from rs_tool import rs_Camera
import cv2

cap = rs_Camera()
model = YOLO("yolov8n.pt")

while True:
	color_image, depth_image = cap.getframe()
	results = model(color_image)
	boxes = results[0].boxes.xyxy
	c = results[0].boxes.cls
	
	img = color_image.copy()
	for b in boxes:

		img = cv2.rectangle(img, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), (0, 0, 0), 2)
	cv2.imshow('Image with Rectangle', img)
	cv2.waitKey(1)
cv2.destroyAllWindows()
