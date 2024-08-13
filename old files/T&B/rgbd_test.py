from ultralytics import YOLO

import cv2
import numpy as np
from rs_tool import rs_Camera


# Load a model
model = YOLO('yolov8n-seg.pt')

cap = rs_Camera()
while True:
	img, depth_frame = cap.getframe()
	depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_frame, alpha=0.03), cv2.COLORMAP_TURBO)
	result = model(img, classes=[0])[0]
	if result:
		name=result.names
		Cls=result.boxes.cls
		masks=result.masks.xy
		#print(name)
		
		
		#print(depth_colormap.shape)
		#print(img.shape)

		for m in masks:
			pts = np.array(m, np.int32)
			pts = pts.reshape((-1, 1, 2))
			cv2.polylines(img, [pts], isClosed=True, color=(0, 0, 0), thickness=2)
			cv2.polylines(depth_colormap, [pts], isClosed=True, color=(0, 0, 0), thickness=2)

	f = np.hstack((img, depth_colormap))
	cv2.imshow("live", f)
	cv2.waitKey(1)
cv2.destroyAllWindows()