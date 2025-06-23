# MusicApp - Core Application File
# Focus: Basic Voice Recording for Solfege Notes

import pyaudio
import wave
import time # To help name unique recording files

# --- Configuration for Audio Recording ---
# These values are standard for good quality audio
FORMAT = pyaudio.paInt16    # Audio format (16-bit integers)
CHANNELS = 1                # Number of audio channels (1 for mono, 2 for stereo)
RATE = 44100                # Sample rate (samples per second, 44.1kHz is standard CD quality)
CHUNK = 1024                # Number of audio frames per buffer
RECORD_SECONDS = 3          # Duration of each recording in seconds (can be adjusted)
OUTPUT_DIR = "recordings/"  # Directory to save recordings (will be created if not exists)

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

    # Find default input device
    # You might need to specify a device index if you have multiple microphones
    # info = audio.get_host_api_info_by_index(0)
    # numdevices = info.get('deviceCount')
    # for i in range(0, numdevices):
    #     if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
    #         print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))
    # Use index based on output from above, or just rely on default

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
    import os
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Save the recorded audio to a WAV file
    # We use a timestamp to ensure unique filenames if you record multiple times
    timestamp = int(time.time())
    file_name = f"{OUTPUT_DIR}{note_name.lower()}_{timestamp}.wav"

    wf = wave.open(file_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"Recording saved to: {file_name}")
    return file_name # Return the path to the saved file


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

    print("\nThanks for using MusicApp! Now you have your recorded solfège notes.")
    print("Next, we can explore playing them back.")