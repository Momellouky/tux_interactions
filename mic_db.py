import sounddevice as sd
import numpy as np
from time import sleep
import time
import socket
import sys
import select


address = ('localhost', 6006)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# Define the duration of each recording in seconds
duration = 0.1

# Define the sampling frequency
fs = 44100

# Define a threshold for high intensity
threshold = 0.2

while True:
    sleep(1/30)
    # Start recording audio from the microphone
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)

    # Wait for the recording to finish
    sd.wait()

    # Calculate the intensity of the recording
    intensity = np.sqrt(np.mean(recording**2))

    # Print the intensity value to the console
    print(f"Microphone intensity: {intensity:.2f}")

    # Check if intensity is above threshold
    if intensity > threshold:
        data = b'RESCUE'
        client_socket.sendto(data, address)

    # Wait for a short interval before starting the next recording
    time.sleep(0.1)
