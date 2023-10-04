from gtts import gTTS
import numpy as np
import soundfile as sf
from scipy.io.wavfile import write
from pydub import AudioSegment

# Your previous code to generate final_wave
rate = 44100
golden_ratio = 1.618033988749895


def generate_pulse_wave(freq, duration, duty_cycle=0.5, rate=44100):
    t = np.linspace(0, duration, int(rate * duration), endpoint=False)
    wave = np.sin(2 * np.pi * freq * t)
    pulse_wave = np.sign(wave - duty_cycle)
    return 0.5 * pulse_wave


def arpeggio(frequencies, duration):
    arpeggio_wave = np.array([])
    note_duration = duration / len(frequencies)
    for freq in frequencies:
        arpeggio_wave = np.concatenate(
            [arpeggio_wave, generate_pulse_wave(freq / 2, note_duration)]
        )
    return arpeggio_wave


final_wave = np.array([])
frequencies = [261.63, 329.63, 392]
current_time = 0

while current_time < 15 * rate:
    segment = arpeggio(frequencies, 0.2)
    final_wave = np.concatenate([final_wave, segment])
    current_time += len(segment)
    frequencies = [freq * golden_ratio for freq in frequencies][:3]

final_wave = final_wave[: int(20 * rate)]
final_wave = np.int16(final_wave * 32767 / np.max(np.abs(final_wave)))

# Generate the speech using Google Text-to-Speech
tts = gTTS(text="SPACIES: A SPACE INVADER CLONE IN RUST", lang="en")
tts.save("speech.mp3")  # Saving the speech to an mp3 file
sound = AudioSegment.from_mp3("speech.mp3")
sound.export("speech.wav", format="wav")  # Convert mp3 to wav

# Read the speech audio
speech_rate, speech_data = sf.read("speech.mp3", dtype="int16")
print(type(speech_data), speech_data)  # Debug line
if len(speech_data.shape) > 1:
    speech_data = speech_data.mean(axis=1)

# Overlay logic here
start_pos = 30 * rate
speech_length = len(speech_data)

if len(final_wave) < start_pos + speech_length:
    padding = np.zeros((start_pos + speech_length) - len(final_wave), dtype="int16")
    final_wave = np.concatenate([final_wave, padding])

final_wave[start_pos : start_pos + speech_length] += speech_data
final_wave = np.int16(final_wave * 32767 / np.max(np.abs(final_wave)))

# Write the final WAV file
sf.write("spacies_theme.wav", final_wave, rate)
