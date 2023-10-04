import numpy as np
from scipy.io.wavfile import write

# Sampling parameters
rate = 44100  # samples per second
T = 3  # sample duration (seconds)
f = 440.0  # frequency (Hz)

# t is the sample index
t = np.linspace(0, T, T * rate, endpoint=False)

# Generate a sine wave
x = 0.5 * np.sin(2 * np.pi * f * t)

# Ensure that highest value is in 16-bit range
audio = np.int16(x * 32767)

# Write the samples to a file
write("sine.wav", rate, audio)
