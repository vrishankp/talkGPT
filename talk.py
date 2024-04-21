from pathlib import Path
from openai import OpenAI
import os
from config import openai_api_key as key
import soundfile as sf
import pyaudio
import requests
import io

def tts(input_text, voice='niva', model='tts-1'):
    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f'Bearer {key}', 
    }

    data = {
        "model": model,
        "input": input_text,
        "voice": voice,
        "response_format": "opus",
    }

    audio = pyaudio.PyAudio()

    def get_pyaudio_format(subtype):
        if subtype == 'PCM_16':
            return pyaudio.paInt16
        return pyaudio.paInt16

    with requests.post(url, headers=headers, json=data, stream=True) as response:
        if response.status_code == 200:
            buffer = io.BytesIO()
            for chunk in response.iter_content(chunk_size=4096):
                buffer.write(chunk)
            
            buffer.seek(0)

            with sf.SoundFile(buffer, 'r') as sound_file:
                format = get_pyaudio_format(sound_file.subtype)
                channels = sound_file.channels
                rate = sound_file.samplerate

                stream = audio.open(format=format, channels=channels, rate=rate, output=True)
                chunk_size = 1024
                data = sound_file.read(chunk_size, dtype='int16')

                while len(data) > 0:
                    stream.write(data.tobytes())
                    data = sound_file.read(chunk_size, dtype='int16')

                stream.stop_stream()
                stream.close()
        else:
            print(f"Error: {response.status_code} : {response.text}")

        audio.terminate()
