import cv2
import numpy as np

def get_brake(cap, sensitivity) :
    ret, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds of red color in HSV color space
    lower_red = np.array([0, sensitivity, sensitivity])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, sensitivity, sensitivity])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    # Combine masks
    mask = cv2.bitwise_or(mask1, mask2)

    # Find contours in the masked image
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #si cube rouge detecté
    if len(contours) > 0:
        return True
    else:
        return False
