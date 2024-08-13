from rs_tool import rs_Camera
import numpy as np
import mediapipe as mp
import cv2

# 初始化MediaPipe Hands模型
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# 使用OpenCV捕获摄像头图像
cap = rs_Camera()

while True:
    frame, depth_image = cap.getframe()
    results = hands.process(frame)
    if results.multi_hand_landmarks:
        landmarks = results.multi_hand_landmarks[0]
        points = landmarks.landmark
        cord = (points[8].x, points[8].y)
        x, y = int(cord[0] * frame.shape[1]), int(cord[1] * frame.shape[0])
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_BONE)
    images = np.hstack((frame, depth_colormap))


    cv2.imshow("Hand Tracking", images)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
