import sounddevice as sd
import numpy as np
import socket
from time import sleep

address = ("localhost", 6006)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

duration = 1/60
threshold = 100
amplification = 1000

print("Mic client started, inputs in 5 seconds")
sleep(5)

while True :
    val = False

    # Define the sampling frequency
    fs = 44100

    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)

    # Wait for the recording to finish
    sd.wait()

    # Calculate the intensity of the recording
    intensity = np.sqrt(np.mean(recording**2))*amplification
    print(intensity)

    # Check if intensity is above threshold
    if intensity > threshold:
        client_socket.sendto(b"P_BRAKE", address)
    else:
        client_socket.sendto(b"R_BRAKE", address)
