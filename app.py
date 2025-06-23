# MusicApp - Core Application File
# Focus: Basic Voice Recording and Playback for Solfege Notes

import pyaudio
import wave
import time # To help name unique recording files
import os   # To manage directory creation and file paths

# --- Configuration for Audio Recording/Playback ---
FORMAT = pyaudio.paInt16    # Audio format (16-bit integers)
CHANNELS = 1                # Number of audio channels (1 for mono, 2 for stereo)
RATE = 44100                # Sample rate (samples per second, 44.1kHz is standard CD quality)
CHUNK = 1024                # Number of audio frames per buffer
RECORD_SECONDS = 1.5          # Duration of each recording in seconds (can be adjusted)
OUTPUT_DIR = "recordings/"  # Directory to save recordings

# The 7-note solfège system
SOLFEGE_NOTES = ["Do", "Re", "Mi", "Fa", "Sol", "La", "Ti"]


def greet_user(name):
    """
    This function greets the user with a personalized message.
    """
    return f"Hello, {name}! Welcome to MusicApp."

def record_note(note_name, duration=RECORD_SECONDS):
    """
    Records audio for a specified duration and saves it to a WAV file.
    """
    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print(f"\n[RECORDING] Please sing '{note_name}' for {duration} seconds...")
    frames = []

    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print(f"[RECORDING] Finished recording '{note_name}'.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Ensure the output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Save the recorded audio to a WAV file
    timestamp = int(time.time())
    file_name = os.path.join(OUTPUT_DIR, f"{note_name.lower()}_{timestamp}.wav") # Use os.path.join for better path handling

    wf = wave.open(file_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"Recording saved to: {file_name}")
    return file_name # Return the path to the saved file

def play_note_file(file_path):
    """
    Plays a WAV audio file.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found for playback: {file_path}")
        return

    print(f"[PLAYBACK] Playing: {file_path}...")
    wf = wave.open(file_path, 'rb') # Open in read-binary mode

    audio = pyaudio.PyAudio()

    stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True) # Important: output=True for playback!

    # Read data in chunks and play it
    data = wf.readframes(CHUNK)
    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)

    print("[PLAYBACK] Playback finished.")

    stream.stop_stream()
    stream.close()
    audio.terminate()
    wf.close()


# Main part of the application
if __name__ == "__main__":
    user_name = input("Please enter your name: ")
    print(greet_user(user_name))

    print("\n--- MusicApp: Solfège Recording Module ---")
    print("We will now record each note of the 7-note solfège scale.")
    print(f"Please sing each note for approximately {RECORD_SECONDS} seconds when prompted.")

    recorded_files = []
    for note in SOLFEGE_NOTES:
        file_path = record_note(note)
        recorded_files.append(file_path)

    print("\n--- All Notes Recorded! ---")
    print("Recordings saved:")
    for f in recorded_files:
        print(f"- {f}")

    # --- New Playback Section ---
    print("\n--- Playback Module ---")
    play_choice = input("Would you like to play back your recorded notes now? (yes/no): ").lower().strip()

    if play_choice == "yes":
        print("\nPlaying back your recorded notes:")
        for note_file in recorded_files:
            play_note_file(note_file)
            time.sleep(0.2) # Small pause between notes for clarity
    else:
        print("Okay, skipping playback for now.")

    print("\nThanks for using MusicApp! Now you have your recorded solfège notes.")
    print("Next, we can explore advanced features like analyzing the notes!")
