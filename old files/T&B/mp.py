import cv2
import numpy as np
import mediapipe as mp


mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                fingertip = hand_landmarks.landmark[5:9]
                angList=[]
                for i in range(len(fingertip)-1):
                	vector = np.array([fingertip[i+1].x-fingertip[i].x, fingertip[i+1].y-fingertip[i].y])
                	y_axis = np.array([0, -1])
                	angle_rad = np.arccos(np.dot(vector, y_axis) / (np.linalg.norm(vector) * np.linalg.norm(y_axis)))
                	angle_deg = np.degrees(angle_rad)
                	if fingertip[i+1].x<fingertip[i].x: angle_deg*=-1
                	angList.append(angle_deg)
                angList[2]-=angList[1]
                angList[1]-=angList[0]
                print(angList)

                for f in fingertip:
                    fingertip_x = int(f.x * frame.shape[1])
                    fingertip_y = int(f.y * frame.shape[0])
                    cv2.circle(frame, (fingertip_x, fingertip_y), 10, (0, 255, 0), -1)
        cv2.imshow('Finger Skeleton Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
cap.release()
cv2.destroyAllWindows()
