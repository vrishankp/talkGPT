import pyaudio
import wave
import threading
import keyboard
import os
from pydub import AudioSegment

def record_audio(file_path, sample_rate=44100, chunk_size=4096, key="space"):
    # Create a PyAudio object
    audio = pyaudio.PyAudio()

    # Set up the audio stream
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk_size)

    frames = []
    recording = True

    def record_audio_thread():
        nonlocal recording
        while recording:
            data = stream.read(chunk_size)
            frames.append(data)

    # Start a separate thread for recording
    record_thread = threading.Thread(target=record_audio_thread)
    record_thread.start()

    print(f"Recording audio. Press '{key}' to stop...")

    # Wait for the specified key press to stop recording
    keyboard.wait(key)

    # Stop the recording thread and close the audio stream
    recording = False
    record_thread.join()
    stream.stop_stream()
    stream.close()
    print("Finished recording.")
    
    # Save the recorded audio as a WAV file
    wav_file = "recorded_audio.wav"
    with wave.open(wav_file, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

    # Convert the WAV file to MP3 using pydub
    mp3_file = file_path
    audio_segment = AudioSegment.from_wav(wav_file)
    audio_segment.export(mp3_file, format="mp3")

    # Clean up the temporary WAV file
    os.remove(wav_file)

    audio.terminate()
    return mp3_file
