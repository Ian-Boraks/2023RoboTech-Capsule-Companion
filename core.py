import speech_recognition as sr
import googletrans
import gtts  
import threading
from io import BytesIO 
from pydub import AudioSegment
from pydub.playback import play
import sys

def setup_microphone():
    r = sr.Recognizer()
    #r.energy_threshold = 4000
    #r.dynamic_energy_threshold = True
    #r.dynamic_energy_adjustment_damping = 0.15
    #r.dynamic_energy_adjustment_ratio = 1.5
    #r.pause_threshold = 0.8
    #r.phrase_threshold = 0.3
    #r.non_speaking_duration = 0.5
    return r

def listen_and_recognize_whisper(r, from_code):
    with sr.Microphone() as source:
        print("listening...")
        audio = r.listen(source)
        try:
            print("recognizing...")
            text = r.recognize_whisper(audio, model="small", language=from_code)
            if len(text) > 0:
                print(text)
                return text
        except:
            print("text not > 0")

def recognize_whisper_from_file(r, file_name, from_code):
    with sr.AudioFile(file_name) as source:
        audio = r.record(source)
        try:
            text = r.recognize_whisper(audio, model="small", language=from_code)
            if len(text) > 0:
                print(text)
                return text
        except:
            print("text not > 0")

def say(text, to_code):
    tts = gtts.gTTS(text, lang=to_code)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    aud = AudioSegment.from_file(fp, format="mp3")
    play(aud)

def main():
    print("Starting...")
    r = setup_microphone()
    while True:
        text = listen_and_recognize_whisper(r, from_code)
        if text:
            print("Spoken: ", text)
