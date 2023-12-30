#!/usr/bin/env python3
# Michael ORTEGA - 09 jan 2018

###############################################################################
## Global libs
import socket
import numpy as np
from time import sleep
import atexit
import cv2
import mediapipe as mp
import csv

from Direction.face_tracking import get_left_right
import FingerCounter.FingerCounter as fc
from cam_red import get_brake
import color_detector.color_detector as cd
import params as p

address = ("localhost", 6006)
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

count_fingers = fc.FingerCounter()

color_detector = cd.Color_Detector()

print("STK input client started, inputs starting in 5 seconds")
sleep(5)

def generate_frame_list(n):
    lst = np.zeros(60, dtype=int)
    if n == 0:
        return lst
    interval = 60 / n
    counter = 0
    for i in range(60):
        if i == round(interval * counter):
            lst[i] = 1
            counter += 1

    return lst

def read_file(file):
    # Create an empty list to store the CSV data
    csv_data = []

    # Open the CSV file and read its contents
    with open(file, newline="", encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile)

        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Assuming each row contains only one value, you can use row[0]
            csv_data.append(row[0])

    return csv_data

def click_space_collaborative(color_name) -> bool:
    arrow = read_file(p.ARROW_FILE)
    bowling_ball = read_file(p.BOWLING_BALL_FILE)
    skimmer = read_file(p.SKIMMER_FILE)
    anchor = read_file(p.ANCHOR_FILE)
    bullet = read_file(p.BULLET_FILE)
    basketball = read_file(p.BASKETBALL_FILE)
    parachute = read_file(p.PARACHUTE_FILE)
    planger = read_file(p.PLANGER_FILE)
    cupcake = read_file(p.CUPCAKE_FILE)

    if color_name in (
        arrow
        or bowling_ball
        or basketball
        or bowling_ball
        or skimmer
        or anchor
        or bullet
        or parachute
        or planger
        or cupcake
    ):
        return True

    return False

def click_space_competitive(color_name) -> bool:
    black_box = read_file(p.BLACK_BOX_FILE)
    if color_name in black_box :
        return True

    return False

# Release resources
def exit_handler():
    cap.release()

atexit.register(exit_handler)

frame_counter = 0

collaboration = True

will_left = False
will_right = False
will_rescue = False
will_brake = False
will_fire = False

while True:  # main loop
    # face detection
    lr_type, lr_value = get_left_right(cap, face_detection)
    print(f"{lr_type}:{lr_value}")

    lr_frames_on = int(lr_value * 60)
    lr_frame_list = generate_frame_list(lr_frames_on)

    if lr_type == "left" :
        will_left = True
        will_right = False
        if lr_frame_list[frame_counter] == 1:  # tourner à gauche
            will_left = True
        else :
            will_left = False
    if lr_type == "right" :
        will_left = False
        will_right = True
        if lr_frame_list[frame_counter] == 1:  # tourner à droite
            will_right = True
        else :
            will_right = False
    else :
        will_left = True
        will_right = False
        if lr_frame_list[frame_counter] == 1:  # tourner à gauche
            will_left = True
        else :
            will_left = False

    # 10 fingers rescue
    if collaboration:
        fingers_value = count_fingers.countFingers(cap)
        if fingers_value >= 10:
            will_rescue = True
        else :
            will_rescue = False

    # brake
    will_brake = get_brake(cap, sensitivity=175)

    # object
    color_name = color_detector.detect_color(cap)
    will_fire = click_space_collaborative(color_name)
    color_name = color_detector.detect_color(cap)
    if collaboration :
        will_fire = click_space_collaborative(color_name)
    else :
        will_fire = click_space_competitive(color_name)

    # send commands
    if will_left:
        client_socket.sendto(b"P_LEFT", address)
    else:
        client_socket.sendto(b"R_LEFT", address)
    if will_right:
        client_socket.sendto(b"P_RIGHT", address)
    else:
        client_socket.sendto(b"R_RIGHT", address)
    if will_rescue:
        client_socket.sendto(b"P_RESCUE", address)
    else:
        client_socket.sendto(b"R_RESCUE", address)
    if will_brake:
        client_socket.sendto(b"P_BRAKE", address)
    else:
        client_socket.sendto(b"R_BRAKE", address)
    if will_fire :
        client_socket.sendto(b"P_FIRE", address)
    else :
        client_socket.sendto(b"P_FIRE", address)

    frame_counter += 1
    frame_counter = frame_counter % 60
    sleep(1 / 60)
