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
        mid=[(int(b[0])+int(b[2]))//2, (int(b[1])+int(b[3]))//2]
        depth = depth_image[mid[1]][mid[0]]
        cord = cap.to_cord(mid[0], mid[1], depth)

        depth_colormap=cv2.putText(depth_colormap, str(depth), (int(b[0]), int(b[1])-25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
        depth_colormap=cv2.putText(depth_colormap, str(cord), (int(b[0]), int(b[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
    img=cv2.hconcat((color_image, depth_colormap))
    cv2.imshow("live", img)
    cv2.waitKey(1)
cv2.destroyAllWindows()