import numpy as np
from scipy.io.wavfile import write


def generate_sine_wave(freq, duration, rate=44100):
    t = np.linspace(0, duration, int(rate * duration), endpoint=False)
    return 0.5 * np.sin(2 * np.pi * freq * t)


# Sampling rate: 44.1 kHz
rate = 44100

# Generate waves of different frequencies
wave1 = generate_sine_wave(440, 0.5)  # A4 note for 0.5 seconds
wave2 = generate_sine_wave(880, 0.5)  # A5 note for 0.5 seconds
wave3 = generate_sine_wave(660, 0.5)  # E5 note for 0.5 seconds
wave4 = generate_sine_wave(220, 0.5)  # A3 note for 0.5 seconds

wave5 = generate_sine_wave(880, 0.5)  # A5 note for 0.5 seconds
wave6 = generate_sine_wave(660, 0.5)  # E5 note for 0.5 seconds
wave7 = generate_sine_wave(220, 0.5)  # A3 note for 0.5 seconds

wave8 = generate_sine_wave(880, 0.5)  # A5 note for 0.5 seconds
wave9 = generate_sine_wave(660, 0.5)  # E5 note for 0.5 seconds
wave10 = generate_sine_wave(220, 0.5)  # A3 note for 0.5 seconds

wave11 = generate_sine_wave(880, 0.25)  # A5 note for 0.25 seconds
wave12 = generate_sine_wave(660, 0.25)  # E5 note for 0.25 seconds
wave13 = generate_sine_wave(880, 0.25)  # A5 note for 0.25 seconds

wave14 = generate_sine_wave(880, 0.25)  # A5 note for 0.25 seconds
wave15 = generate_sine_wave(660, 0.25)  # E5 note for 0.25 seconds
wave16 = generate_sine_wave(880, 0.25)  # A5 note for 0.25 seconds

wave17 = generate_sine_wave(880, 0.25)  # A5 note for 0.25 seconds
wave18 = generate_sine_wave(660, 0.25)  # E5 note for 0.25 seconds
wave19 = generate_sine_wave(880, 0.25)  # A5 note for 0.25 seconds

wave20 = generate_sine_wave(880, 0.25)  # A5 note for 0.25 seconds
wave21 = generate_sine_wave(660, 0.25)  # E5 note for 0.25 seconds
wave22 = generate_sine_wave(880, 0.25)  # A5 note for 0.25 seconds

wave23 = generate_sine_wave(880, 0.25)  # A5 note for 0.25 seconds
wave24 = generate_sine_wave(660, 0.25)  # E5 note for 0.25 seconds
wave25 = generate_sine_wave(880, 0.25)  # A5 note for 0.25 seconds

wave26 = generate_sine_wave(440, 3.0)  # A4 note for 3.0 seconds


# Concatenate the waves to create a sequence
final_wave = np.concatenate(
    [
        wave1,
        wave2,
        wave3,
        wave4,
        wave5,
        wave6,
        wave7,
        wave8,
        wave9,
        wave10,
        wave11,
        wave12,
        wave13,
        wave14,
        wave15,
        wave16,
        wave17,
        wave18,
        wave19,
        wave20,
        wave21,
        wave22,
        wave23,
        wave24,
        wave25,
        wave26,
    ]
)

# Convert to 16-bit PCM format
final_wave = np.int16(final_wave * 32767)

# Write the WAV file
write("startup_sound.wav", rate, final_wave)
