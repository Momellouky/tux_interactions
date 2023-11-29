#!/usr/bin/env python3
#Michael ORTEGA - 09 jan 2018

###############################################################################
## Global libs
import serial
import socket
import numpy as np
from time import sleep

address = ('localhost', 6006)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# replace COM5 with whichever serial port the Arduino is connected to
arduino = serial.Serial(port='COM5', baudrate=9600, timeout=1)

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

frame_counter = 0

will_acc = False
will_dri = False

while True: # main loop
    poll_type, poll_value = poll_input()

    frames_on = int(poll_value*60)
    frame_list = generate_frame_list(frames_on)

    if poll_type == "acc" : #accélération
        if frame_list[frame_counter] == 1 :
            will_acc = True
        else :
            will_acc = False
    elif poll_type == "dri" : #drift
        if poll_value == 1 :
            will_dri = True
        else :
            will_dri = False
    
    # send commands
    if will_acc :
        client_socket.sendto(b'P_ACCELERATE', address)
    else :
        client_socket.sendto(b'R_ACCELERATE', address)
    if will_dri :
        client_socket.sendto(b'P_SKIDDING', address)
    else :
        client_socket.sendto(b'R_SKIDDING', address)

    frame_counter += 1
    frame_counter = frame_counter % 60
    sleep(1/60)

# TODO : proper way to end script that closes connection to serial port
# currently, we need to unplug and replug the Arduino to be able to relaunch the script