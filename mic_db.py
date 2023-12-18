import sounddevice as sd
import numpy as np

def get_rescue(duration, threshold) :
    val = False

    # Define the sampling frequency
    fs = 44100

    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)

    # Wait for the recording to finish
    sd.wait()

    # Calculate the intensity of the recording
    intensity = np.sqrt(np.mean(recording**2))*1000

    # Check if intensity is above threshold
    if intensity > threshold:
        val = True
    
    return val
