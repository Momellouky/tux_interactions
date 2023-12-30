import serial
from time import sleep
import numpy as np
import atexit
import socket

arduino = serial.Serial(port="COM5", baudrate=9600, timeout=1)

address = ("localhost", 6006)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def poll_input():
    data = arduino.readline()
    #arduino.reset_input_buffer()
    #print(data)
    try :
        data = data[0:-2]
        data_type = str(data[0:3])
        data_type = data_type[2:-1]
        data_value = float(data[4:8])
    except : 
        return "err", 0
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

def exit_handler():
    arduino.close()

atexit.register(exit_handler)

print("Arduino client started, starting inputs in 5 seconds")
sleep(5)

frame_counter = 0
will_acc = False
will_dri = False
will_bst = False

while True :
    # arduino
    poll_type, poll_value = poll_input()

    poll_frames_on = int(poll_value * 60)
    poll_frame_list = generate_frame_list(poll_frames_on)

    if poll_type == "acc" : # accélération
        if poll_frame_list[frame_counter] == 1:
            will_acc = True
        else :
            will_acc = False
    if poll_type == "dri" and poll_value == 1:  # drift
        if poll_value == 1 :
            will_dri = True
        else :
            will_dri = False
    if poll_type == "bst" :
        if  poll_value == 1:  # boost
            will_bst = True
        else :
            will_bst = False

    # send commands
    if will_acc:
        client_socket.sendto(b"P_ACCELERATE", address)
    else:
        client_socket.sendto(b"R_ACCELERATE", address)
    if will_dri:
        client_socket.sendto(b"P_SKIDDING", address)
    else:
        client_socket.sendto(b"R_SKIDDING", address)
    if will_bst:
        client_socket.sendto(b"P_NITRO", address)
    else:
        client_socket.sendto(b"R_NITRO", address)


    frame_counter += 1
    frame_counter = frame_counter % 60
    sleep(1 / 60)
