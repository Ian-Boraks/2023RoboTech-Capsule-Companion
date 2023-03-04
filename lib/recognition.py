import speech_recognition as sr
import whisper
import sys
from pydub import AudioSegment
from pydub.playback import play

from .chat import add_message, reset_messages
from .speech import say

r = sr.Recognizer()
model = whisper.load_model("small.en")

state = "listening"

def init_recognizer(source: sr.AudioSource):
    print("Adjusting...")
    r.adjust_for_ambient_noise(source, duration=1)

def transcribe(source: sr.AudioSource):
    if state == "command" or state == "repeat":
        afile = AudioSegment.from_wav("assets/beep.wav")
        play(afile)
    print("Listening...")
    audio = r.listen(source)
    with open("temp.wav", "wb") as f:
        f.write(audio.get_wav_data())
        f.flush()
        print("Recognizing...")
        result = model.transcribe(f.name)
        return result["text"]

def handle_listening(text: str):
    if "buzz" in text:
        say("yes?")
        return "command"
    return "listening"

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
    return "listening"

def handle_therapy(text: str):
    if "exit" in text:
        reset_messages()
        say("ending session")
        return "listening"
    print("Generating Response...")
    res = add_message(text)
    print("Response:", res)
    say(res)
    return "therapy"

def next_state(source: sr.AudioSource):
    global state
    text = transcribe(source).lower()
    print("Heard:", text)

    if text:
        if state == "listening":
            state = handle_listening(text)
        elif state == "command":
            state = handle_command(text)
        elif state == "repeat":
            state = handle_repeat(text)
        elif state == "therapy":
            state = handle_therapy(text)
