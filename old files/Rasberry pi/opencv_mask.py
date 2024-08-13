import cv2
import numpy as np
from picamera2 import Picamera2


def getBlueCenter(hsv):
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    one_indices = np.argwhere(mask == 255)
    center = np.mean(one_indices, axis=0)

    try:
        return (int(center[1]), int(center[0]))
    except:
        return []

def getRedCenter(hsv):
    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = cv2.bitwise_or(mask1, mask2)
    one_indices = np.argwhere(mask == 255)
    center = np.mean(one_indices, axis=0)
    #cv2.imshow('mask', mask)
    try:
        return (int(center[1]), int(center[0]))
    except:
        return []

def getYellowCenter(hsv):
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    one_indices = np.argwhere(mask == 255)
    center = np.mean(one_indices, axis=0)
    try:
        return (int(center[1]), int(center[0]))
    except:
        return []

def getGreenCenter(hsv):
    lower_green = np.array([40, 50, 50])
    upper_green = np.array([80, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    one_indices = np.argwhere(mask == 255)
    center = np.mean(one_indices, axis=0)

    try:
        return (int(center[1]), int(center[0]))
    except:
        return []

if __name__=='__main__':
    picam2 = Picamera2()
    picam2.start()

    while(True):
        frame = picam2.capture_array()
        bgr=cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        
        center=getRedCenter(hsv)
        if len(center)>0:
            center = (int(center[1]), int(center[0]))
            cv2.circle(bgr, center, 5, (0, 255, 0), -1)

        #mask_3d=np.stack((mask, mask, mask), axis=2)
        #show=np.vstack((mask_3d, bgr))
        cv2.imshow('live', bgr)

        if cv2.waitKey(1) == ord('q'): break

    cv2.destroyAllWindows()
