import numpy as np
from scipy.io.wavfile import write

# Constants
rate = 44100  # Sample rate
golden_ratio = 1.618033988749895


def generate_pulse_wave(freq, duration, duty_cycle=0.5, rate=44100):
    t = np.linspace(0, duration, int(rate * duration), endpoint=False)
    wave = np.sin(2 * np.pi * freq * t)
    pulse_wave = np.sign(wave - duty_cycle)
    return 0.5 * pulse_wave


# Function to create an arpeggio
def arpeggio(frequencies, duration):
    arpeggio_wave = np.array([])
    note_duration = duration / len(frequencies)
    for freq in frequencies:
        arpeggio_wave = np.concatenate(
            [arpeggio_wave, generate_pulse_wave(freq / 2, note_duration)]
        )  # Octave lower
    return arpeggio_wave


# Initialize empty audio track
final_wave = np.array([])

# Frequencies for the arpeggios (example: C E G for C major chord)
frequencies = [261.63, 329.63, 392]

# Create cascading arpeggios
current_time = 0
while current_time < 15 * rate:  # Ensuring the length is at least 15 seconds
    # Append the arpeggio and move the time marker
    segment = arpeggio(frequencies, 0.2)
    final_wave = np.concatenate([final_wave, segment])
    current_time += len(segment)

    # Overlay the next arpeggio, increasing the pitch slightly (multiplying by golden_ratio)
    frequencies = [freq * golden_ratio for freq in frequencies][
        :3
    ]  # Keep only the first three frequencies

# Trim and normalize the final_wave to make it 15 to 20 seconds
final_wave = final_wave[: int(20 * rate)]
final_wave = np.int16(
    final_wave * 32767 / np.max(np.abs(final_wave))
)  # Normalize to 16-bit

# Write the WAV file
write("startup_theme_pulse_wave.wav", rate, final_wave)
