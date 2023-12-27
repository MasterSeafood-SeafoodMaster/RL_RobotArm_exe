from rs_tool import rs_Camera
from ultralytics import YOLO
import cv2
import numpy as np
model = YOLO("best.pt")
cap = rs_Camera()
while True:
    color_image, depth_image = cap.getframe()
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
    results=model(color_image, conf=0.5)
    boxes=results[0].boxes.xyxy
    for b in boxes:
        color_image=cv2.rectangle(color_image, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), (0, 255, 0), 2)
        depth_colormap=cv2.rectangle(depth_colormap, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), (0, 255, 0), 2)
    img=cv2.hconcat((color_image, depth_colormap))
    cv2.imshow("live", img)
    cv2.waitKey(1)
cv2.destroyAllWindows()