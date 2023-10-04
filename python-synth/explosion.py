import numpy as np
from scipy.io.wavfile import write


def generate_noise(duration, rate=44100):
    return np.random.uniform(-0.5, 0.5, int(rate * duration))


def generate_explosion_wave(freq, duration, rate=44100):
    t = np.linspace(0, duration, int(rate * duration), endpoint=False)
    sine_wave = np.sin(2 * np.pi * freq * t)
    modulated_wave = sine_wave * np.exp(-5 * t)  # Exponential decay for shockwave feel
    return modulated_wave


# Generate noise wave for crackle effect
noise_wave = generate_noise(0.5)

# Generate explosion waves
explosion_wave_low = generate_explosion_wave(100, 0.5)
explosion_wave_high = generate_explosion_wave(400, 0.5)

# Combine all the waves to create a composite explosion sound
final_explosion_wave = noise_wave + explosion_wave_low + explosion_wave_high

# Normalize the wave
final_explosion_wave = final_explosion_wave / np.max(np.abs(final_explosion_wave))

# Convert to 16-bit PCM format
final_explosion_wave = np.int16(final_explosion_wave * 32767)

# Write the WAV file
write("explosion.wav", 44100, final_explosion_wave)
