import cv2
import numpy as np

# Initialize video capture object
cap = cv2.VideoCapture(0)

lower_red_vb = 115
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds of red color in HSV color space
    lower_red = np.array([0, lower_red_vb, lower_red_vb])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, lower_red_vb, lower_red_vb])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    # Combine masks
    mask = cv2.bitwise_or(mask1, mask2)

    # Find contours in the masked image
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through contours and draw bounding box around red object
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 200:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # Display resulting image
    cv2.imshow('frame', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
