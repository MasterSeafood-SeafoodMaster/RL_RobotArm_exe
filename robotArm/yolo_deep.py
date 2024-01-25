from rs_tool import rs_Camera
import cv2
import numpy as np

from ultralytics import YOLO
model = YOLO("best.pt")
cap = rs_Camera()

while True:
    color_image, depth_image = cap.getframe()
    results=model(color_image)
    #print(results[0].boxes)
    boxes=results[0].boxes.xyxy.tolist()
    print(boxes)

    cord = cap.to_cord(320, 240, depth_image[240][320])
    
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
    img = np.hstack((color_image, depth_colormap))
    cv2.imshow("live", img)
    cv2.waitKey(1)
cv2.destroyAllWindows()