import numpy as np
from scipy.io.wavfile import write


def generate_sine_wave(freq, duration, rate=44100):
    t = np.linspace(0, duration, int(rate * duration), endpoint=False)
    return 0.5 * np.sin(2 * np.pi * freq * t)


# Generate waves of different frequencies
wave1 = generate_sine_wave(440, 0.5)  # 5th fret of high e string (A)
wave2 = generate_sine_wave(493.88, 0.5)  # 7th fret of high e string (B)
wave3 = generate_sine_wave(392, 0.5)  # 8th fret of B string (G)
wave4 = generate_sine_wave(293.66, 0.5)  # 7th fret of G string (D)
wave5 = generate_sine_wave(392, 0.5)  # 5th fret of D string (G)

# Concatenate the waves to create a sequence
final_wave = np.concatenate([wave1, wave2, wave3, wave4, wave5])

# Convert to 16-bit PCM format
final_wave = np.int16(final_wave * 32767)

# Write the WAV file
write("close_encounters.wav", 44100, final_wave)
