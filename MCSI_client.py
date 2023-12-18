#!/usr/bin/env python3
#Michael ORTEGA - 09 jan 2018

###############################################################################
## Global libs
import serial
import socket
import numpy as np
from time import sleep
import atexit
import cv2
import mediapipe as mp

from Direction.face_tracking import get_left_right
from mic_db import get_rescue

address = ('localhost', 6006)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# replace COM5 with whichever serial port the Arduino is connected to
arduino = serial.Serial(port='COM5', baudrate=9600, timeout=1)

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Create a face detection instance
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Get the width of the frame
frame_width = int(cap.get(3))

print("STK input client started")

def poll_input() :
    data = arduino.readline()
    data = data[0:-2]
    data_type = str(data[0:3])
    data_type = data_type[2:-1]
    data_value = float(data[4:8])
    return data_type, data_value

def generate_frame_list(n) :
    lst = np.zeros(60, dtype=int)
    if n == 0 :
        return lst
    interval = 60 / n
    counter = 0
    for i in range(60):
        if i == round(interval * counter):
            lst[i] = 1
            counter += 1

    return lst

# Release resources
def exit_handler():
    cap.release()
    arduino.close()

atexit.register(exit_handler)

frame_counter = 0

while True: # main loop
    will_acc = False
    will_dri = False
    will_left = False
    will_right = False

    # arduino
    poll_type, poll_value = poll_input()

    poll_frames_on = int(poll_value*60)
    poll_frame_list = generate_frame_list(poll_frames_on)

    if poll_type == "acc" and poll_frame_list[frame_counter] == 1 : #accélération
        will_acc = True
    elif poll_type == "dri" and poll_value == 1 : #drift
        will_dri = True
    
    # face detection
    lr_type, lr_value = get_left_right(cap, face_detection)

    lr_frames_on = int(lr_value*60)
    lr_frame_list = generate_frame_list(lr_frames_on)

    if lr_type == "left" and lr_frame_list[frame_counter] == 1 : #tourner à gauche
        will_left = True
    elif lr_type == "right" and lr_frame_list[frame_counter] == 1 : #tourner à droite
        will_right = True

    # microphone
    will_rescue = get_rescue(duration=1/120, threshold=0.5) # 1/120 is an arbitrary value to make sure this loop doesnt take too much time

    # send commands
    if will_acc :
        client_socket.sendto(b'P_ACCELERATE', address)
    else :
        client_socket.sendto(b'R_ACCELERATE', address)
    if will_dri :
        client_socket.sendto(b'P_SKIDDING', address)
    else :
        client_socket.sendto(b'R_SKIDDING', address)
    if will_left :
        client_socket.sendto(b'P_LEFT', address)
    else :
        client_socket.sendto(b'R_LEFT', address)
    if will_right :
        client_socket.sendto(b'P_RIGHT', address)
    else :
        client_socket.sendto(b'R_RIGHT', address)
    if will_rescue :
        client_socket.sendto(b'P_RESCUE', address)
    else :
        client_socket.sendto(b'R_RESCUE', address)

    frame_counter += 1
    frame_counter = frame_counter % 60
    sleep(1/60)
