import numpy as np
from scipy.io.wavfile import write


def generate_sine_wave(freq, duration, rate=44100):
    t = np.linspace(0, duration, int(rate * duration), endpoint=False)
    return 0.5 * np.sin(2 * np.pi * freq * t)


# Array of wave properties: (frequency, duration)
wave_props = (
    [
        (440, 0.25),
        (880, 0.5),
        (660, 0.5),
        (220, 0.5),
    ]
    * 3
    + [(880, 0.25), (660, 0.25), (880, 0.25)] * 7
    + [(440, 3.0)]
)

# Generate and concatenate the waves
final_wave = np.concatenate(
    [generate_sine_wave(freq, duration) for freq, duration in wave_props]
)

# Convert to 16-bit PCM format
final_wave = np.int16(final_wave * 32767)

# Write the WAV file
write("startup_theme.wav", 44100, final_wave)
