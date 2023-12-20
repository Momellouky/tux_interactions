#!/usr/bin/env python3
# Michael ORTEGA - 09 jan 2018

###############################################################################
## Global libs
import serial
import socket
import numpy as np
from time import sleep
import atexit
import cv2
import mediapipe as mp
import csv

from Direction.face_tracking import get_left_right
from mic_db import get_rescue
import FingerCounter.FingerCounter as fc
from cam_red import get_brake
import color_detector.color_detector as cd
import params as p

address = ("localhost", 6006)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# replace COM5 with whichever serial port the Arduino is connected to
arduino = serial.Serial(port="COM5", baudrate=9600, timeout=1)

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

print("STK input client started")


def poll_input():
    data = arduino.readline()
    data = data[0:-2]
    data_type = str(data[0:3])
    data_type = data_type[2:-1]
    data_value = float(data[4:8])
    return data_type, data_value


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

def click_space(color_name) -> bool:
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

# Release resources
def exit_handler():
    cap.release()
    arduino.close()

atexit.register(exit_handler)

frame_counter = 0

collaboration = True

while True:  # main loop
    will_acc = False
    will_dri = False
    will_left = False
    will_right = False
    will_bst = False
    will_rescue = False
    will_brake = False
    will_fire = False

    # arduino
    poll_type, poll_value = poll_input()

    poll_frames_on = int(poll_value * 60)
    poll_frame_list = generate_frame_list(poll_frames_on)

    if poll_type == "acc" and poll_frame_list[frame_counter] == 1:  # accélération
        will_acc = True
    elif poll_type == "dri" and poll_value == 1:  # drift
        will_dri = True
    elif poll_type == "bst" and poll_value == 1:  # boost
        will_bst = True

    # face detection
    lr_type, lr_value = get_left_right(cap, face_detection)

    lr_frames_on = int(lr_value * 60)
    lr_frame_list = generate_frame_list(lr_frames_on)

    if lr_type == "left" and lr_frame_list[frame_counter] == 1:  # tourner à gauche
        will_left = True
    elif lr_type == "right" and lr_frame_list[frame_counter] == 1:  # tourner à droite
        will_right = True

    # microphone rescue
    if not collaboration:
        will_rescue = get_rescue(
            duration=1 / 90, threshold=0.5, amplification=10000
        )  # 1/90 is an arbitrary value to make sure this loop doesnt take too much time

    # 10 fingers rescue
    if collaboration:
        fingers_value = count_fingers.countFingers(cap)
        if fingers_value >= 10:
            will_rescue = True

    # brake
    will_brake = get_brake(cap, sensitivity=150)

    # object
    color_name = color_detector.detect_color(cap)
    will_fire = click_space(color_name)

    # send commands
    if will_acc:
        client_socket.sendto(b"P_ACCELERATE", address)
    else:
        client_socket.sendto(b"R_ACCELERATE", address)
    if will_dri:
        client_socket.sendto(b"P_SKIDDING", address)
    else:
        client_socket.sendto(b"R_SKIDDING", address)
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
    if will_bst:
        client_socket.sendto(b"P_BOOST", address)
    else:
        client_socket.sendto(b"R_BOOST", address)
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
