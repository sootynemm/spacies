import numpy as np
from scipy.io.wavfile import write


def generate_pulse_wave(freq, duration, rate=44100, duty_cycle=0.5):
    t = np.linspace(0, 1, int(rate * duration), endpoint=False)
    return 0.5 * np.sign(np.sin(2 * np.pi * freq * t / duty_cycle))


# Define frequencies for a simplified "Close Encounters" theme
frequencies = [440, 493.88, 392]  # A, B, G

# Generate the pulse waves
waves = [generate_pulse_wave(f, 0.5) for f in frequencies]

# Generate a diminishing fifth sound
# From G (392 Hz) to D (293.66 Hz)
dim_fifth = generate_pulse_wave(392, 0.5)  # Starting note (G)
dim_fifth = np.concatenate(
    [dim_fifth, generate_pulse_wave(293.66, 1.0)]
)  # Falling to D

# Concatenate the waves and the diminishing fifth sound
final_wave = np.concatenate(waves + [dim_fifth])

# Convert to 16-bit PCM format
final_wave = np.int16(final_wave * 32767)

# Write the WAV file
write("losing_retro.wav", 44100, final_wave)
