from rs_tool import rs_Camera
import cv2
import numpy as np

from ultralytics import YOLO
model = YOLO("yolov8n.pt")

cap = rs_Camera()
while True:
    color_image, depth_image = cap.getframe()
    results=model(color_image)
    print(results)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
    img = np.hstack((color_image, depth_colormap))
    cv2.imshow("live", img)
    cv2.waitKey(1)
cv2.destroyAllWindows()