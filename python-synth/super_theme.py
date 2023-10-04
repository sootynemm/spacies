from pydub import AudioSegment
from pydub.generators import Sine

# Initialize an empty audio segment
song = AudioSegment.silent(duration=0)


# Function to create a note
def create_note(frequency, duration):
    return Sine(frequency).to_audio_segment(duration=duration).fade_in(10).fade_out(10)


# Function to create a chord from a list of frequencies
def create_chord(frequencies, duration):
    chord = AudioSegment.silent(duration=duration)
    for freq in frequencies:
        chord = chord.overlay(create_note(freq, duration))
    return chord


# Add a 'space opera' chord inspired by Star Wars (A major: A C# E)
song += create_chord([440, 554.37, 659.25], 1000)

# Add a simple two-note pattern inspired by Commander Keen
song += create_note(880, 300)
song += create_note(440, 300)

# Add the "Close Encounters" inspired riff (A B G)
for freq in [440, 493.88, 392]:
    song += create_note(freq, 500)

# Add a James Bond-inspired falling riff (E D C B)
for freq in [659.25, 587.33, 523.25, 493.88]:
    song += create_note(freq, 250)

# Fill in the rest of the time to make it about 15 seconds
remaining_time = 15000 - len(song)
song += AudioSegment.silent(duration=remaining_time)

# Export the final composition
song.export("super_theme.wav", format="wav")
