import warnings
warnings.filterwarnings("ignore")

import whisper
from config import openai_api_key, groq_api_key
from record import record_audio 
from process import get_chatgpt_response, get_groq_response
import os
from colorama import Fore, Style, Back
from talk import tts

while True:
    file = record_audio("test.mp3")

    #file = "audio.mp3"

    model = whisper.load_model("tiny")
    result = model.transcribe(file, fp16=False)
    os.remove("test.mp3")
    print("Asked: " + result["text"])
    full_text = "Answer this question in 1 sentence: " + result["text"]

    #response = get_chatgpt_response(result["text"], openai_api_key)
    response = get_groq_response(full_text, groq_api_key)
    print(Fore.GREEN + response + Fore.RESET)

    

    tts(response, voice = "shimmer", model = "tts-1")