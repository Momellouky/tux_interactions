import cv2
import mediapipe as mp
from oscpy.client import OSCClient
import pyautogui
import socket
import sys
import select
from time import sleep

address = ('localhost', 6006)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Create a face detection instance
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Get the width of the frame
frame_width = int(cap.get(3))

#client = OSCClient("127.0.0.1", 8000)

# Main loop for face detection
while cap.isOpened():
    sleep(1/60)
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame for face detection
    results = face_detection.process(rgb_frame)

    if results.detections:
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            x_center = bboxC.xmin + bboxC.width / 2

            # Determine if the face is on the left or right
            if x_center < 0.4:
                pressBtn = b'P_RIGHT'
                releaseBtn = b'R_LEFT'
                position = "Right"
                client_socket.sendto(pressBtn, address)
              
                client_socket.sendto(releaseBtn, address)
              
                # Simulate turning right in the game
                #pyautogui.press('right')
            elif x_center > 0.6:
                pressBtn = b'P_LEFT'
                releaseBtn = b'R_RIGHT'
                position = "Left"
                client_socket.sendto(pressBtn, address)
                
                client_socket.sendto(releaseBtn, address)
                # Simulate turning left in the game
                #pyautogui.press('left')
            else:
                releaseBtn = b'R_RIGHT'
                client_socket.sendto(releaseBtn, address)
                releaseBtn = b'R_LEFT'
                
                client_socket.sendto(releaseBtn, address)
               
                position = "Center"
                
                # Simulate going straight in the game
                #pyautogui.press('up')

            # Send OSC message to the server
            #client.send_message(b'/face/position', position.encode())

            # Draw bounding box
            ih, iw, _ = frame.shape
            x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Print the face position
            print(f"Face Position: {position}")

    # Display the frame
    cv2.imshow("Face Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
