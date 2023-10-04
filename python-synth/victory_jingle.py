import numpy as np
from scipy.io.wavfile import write

# Generate square wave
def generate_square_wave(freq, duration, rate=44100):
    t = np.linspace(0, duration, int(rate * duration), endpoint=False)
    sine_wave = np.sin(2 * np.pi * freq * t)
    square_wave = np.sign(sine_wave)
    return square_wave

# Generate sawtooth wave
def generate_sawtooth_wave(freq, duration, rate=44100):
    t = np.linspace(0, duration, int(rate * duration), endpoint=False)
    sawtooth_wave = 0.5 * (1.0 - np.mod(t * freq, 1.0))
    return sawtooth_wave

# Melody and duration tuples for square wave instrument (Inspired by classic 8-bit games)
melody_square = [
    (440, 0.2),
    (440, 0.2),
    (0, 0.1),
    (440, 0.2),
    (0, 0.1),
    (880, 0.4),
]

# Melody and duration tuples for sawtooth wave instrument
melody_sawtooth = [
    (220, 0.2),
    (220, 0.2),
    (0, 0.1),
    (220, 0.2),
    (0, 0.1),
    (660, 0.4),
]

# Generate the square and sawtooth waveforms
square_wave = np.concatenate([generate_square_wave(f, d) for f, d in melody_square])
sawtooth_wave = np.concatenate([generate_sawtooth_wave(f, d) for f, d in melody_sawtooth])

# Normalize individual waves
square_wave = 0.5 * square_wave / np.max(np.abs(square_wave))
sawtooth_wave = 0.5 * sawtooth_wave / np.max(np.abs(sawtooth_wave))

# Combine them for a richer sound
final_wave = square_wave + sawtooth_wave

# Normalize the final wave
final_wave = final_wave / np.max(np.abs(final_wave))

# Loop the sound to make it 8-16 seconds long
loops = int(12 // (len(final_wave) / 44100))  # Aim for approximately 12 seconds
final_wave = np.tile(final_wave, loops)

# Convert to 16-bit PCM format
final_wave = np.int16(final_wave * 32767)

# Write the WAV file
write("victory_jingle.wav", 44100, final_wave)
