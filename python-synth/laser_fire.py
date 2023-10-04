import numpy as np
from scipy.io.wavfile import write


def generate_pulse_wave(freq, duration, rate=44100):
    t = np.linspace(0, duration, int(rate * duration), endpoint=False)
    sine_wave = np.sin(2 * np.pi * freq * t)
    pulse_wave = np.sign(sine_wave)
    return 0.5 * pulse_wave


# Array of wave properties for a single shot: (frequency, duration)
# Using a higher frequency for that laser-like pitch and a short duration for quick pulse
single_shot_props = [
    (1600, 0.01),  # High pitch start
    (1200, 0.01),  # Lower pitch end
    (0, 0.03),  # Silence to separate from next shot
]

# Generate and concatenate the waves for a single shot
single_shot_wave = np.concatenate(
    [generate_pulse_wave(freq, duration) for freq, duration in single_shot_props]
)

# Duplicate the single shot 12 times to simulate 12 shots fired in rapid succession
final_wave = np.tile(single_shot_wave, 12)

# Convert to 16-bit PCM format
final_wave = np.int16(final_wave * 32767)

# Write the WAV file
write("laser_fire.wav", 44100, final_wave)
