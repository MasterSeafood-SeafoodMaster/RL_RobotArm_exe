from rs_tool import rs_Camera
from ultralytics import YOLO
import cv2
import numpy as np
model = YOLO("best.pt")
cap = rs_Camera()

def to_3D(fx, fy, depth, cx, cy, u, v):
    x = (u-cx)*depth/fx
    y = (v-cy)*depth/fy
    z = depth
    x = np.expand_dims(x, axis = -1)
    y = np.expand_dims(y, axis = -1)
    z = np.expand_dims(z, axis = -1)
    return np.concatenate((x,y,z), axis=-1)


while True:
    color_image, depth_image = cap.getframe()
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
    results=model(color_image, conf=0.5)
    boxes=results[0].boxes.xyxy
    for b in boxes:
        color_image=cv2.rectangle(color_image, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), (0, 255, 0), 2)
        depth_colormap=cv2.rectangle(depth_colormap, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), (0, 255, 0), 2)
        mid=[(int(b[0])+int(b[2]))//2, (int(b[1])+int(b[3]))//2]
        coor=to_3D(mid[0], mid[1], depth_image[mid[1]][mid[0]])

        depth_colormap=cv2.putText(depth_colormap, str(depth_image[mid[1]][mid[0]]), (int(b[0]), int(b[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
    img=cv2.hconcat((color_image, depth_colormap))
    cv2.imshow("live", img)
    cv2.waitKey(1)
cv2.destroyAllWindows()