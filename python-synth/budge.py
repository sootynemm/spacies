import numpy as np
from scipy.io.wavfile import write


def generate_slide_wave(start_freq, end_freq, duration, rate=44100):
    t = np.linspace(0, duration, int(rate * duration), endpoint=False)
    freq = np.linspace(start_freq, end_freq, int(rate * duration))
    slide_wave = np.sin(2 * np.pi * freq * t)
    return slide_wave


# Array of wave properties for "budge" sound: (start_frequency, end_frequency, duration)
# Using a sliding frequency to create a "budge" effect
slide_props = [
    (400, 600, 0.05),
    (600, 400, 0.05),
    (0, 0, 0.05),  # Silence to separate from next sound
]

# Generate and concatenate the waves
budge_wave = np.concatenate(
    [
        generate_slide_wave(start_freq, end_freq, duration)
        for start_freq, end_freq, duration in slide_props
    ]
)

# Normalize the wave
budge_wave = budge_wave / np.max(np.abs(budge_wave))

# Convert to 16-bit PCM format
budge_wave = np.int16(budge_wave * 32767)

# Write the WAV file
write("budge.wav", 44100, budge_wave)
