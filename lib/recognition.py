import speech_recognition as sr
import whisper
import sys
from pydub import AudioSegment
from pydub.playback import play

from .chat import add_message, reset_messages
from .speech import say

r = sr.Recognizer()
'''
Designed by The Psychedelic Psychiatrist
Robo-Tech 2023 @ GT
'''

model = whisper.load_model("small.en")

state = "idle"

def init_recognizer(source: sr.AudioSource):
    print("Adjusting...")
    r.adjust_for_ambient_noise(source, duration=1)

def transcribe(source: sr.AudioSource, beep=False):
    if beep:
        afile = AudioSegment.from_wav("assets/beep.wav")
        play(afile)
    print("Listening...")
    audio = r.listen(source)
    with open("temp.wav", "wb") as f:
        f.write(audio.get_wav_data())
        f.flush()
        print("Recognizing...")
        result = model.transcribe(f.name)
        print("Heard:", result["text"])
        return result["text"].lower()

def handle_command(text: str):
    if "exit" in text:
        say("exiting")
        sys.exit()
    elif "repeat" in text:
        say("enter your speech")
        return "repeat"
    elif "therapy" in text:
        say("welcome to your therapy session!")
        return "therapy"
    return "command"

def handle_repeat(text: str):
    say(text)
    return "idle"

def handle_therapy(text: str):
    if "end session" in text:
        reset_messages()
        say("ending session")
        return "idle"
    print("Generating Response...")
    res = add_message(text)
    print("Response:", res)
    say(res)
    return "therapy"

def run_therapy(source: sr.AudioSource, time: str):
    hour = int(time[:2])
    timestr = ""
    if hour > 11:
        timestr = f"{hour - 12}{time[2:]} PM"
    else:
        timestr = f"{time} AM"
    say(f"Welcome to your {timestr} therapy session!")

    global state
    state = "therapy"
    while state != "idle":
        text = transcribe(source)
        if text:
            state = handle_therapy(text)

def run_command(source: sr.AudioSource):
    global state
    state = "command"
    while state != "idle":
        beep = state == "command" or state == "repeat"
        text = transcribe(source, beep)

        if text:
            if state == "command":
                state = handle_command(text)
            elif state == "repeat":
                state = handle_repeat(text)
            elif state == "therapy":
                state = handle_therapy(text)
