import gtts
import speech_recognition as sr
import whisper
import sys
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

r = sr.Recognizer()
model = whisper.load_model("small.en")
lang = "en"

state = "listening"

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
        return result["text"]

def say(text: str):
    tts = gtts.gTTS(text, lang=lang)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    aud = AudioSegment.from_file(fp, format="mp3")
    play(aud)

def handle_listening(text: str):
    if "buzz" in text:
        say("yes?")
        return "command"

def handle_command(text: str):
    if "exit" in text:
        say("exiting")
        sys.exit()
    elif "talking" in text:
        say("enter your speech")
        return "speech"
    return "command"

def handle_speech(text: str):
    say(text)
    return "listening"
    
def start_loop():
    with sr.Microphone() as source:
        print("Adjusting...")
        r.adjust_for_ambient_noise(source, duration=1)
        
        while True:
            text = transcribe(source, "en").lower()
            print("Heard:", text)

            if text:
                if state == "listening":
                    state = handle_listening(text)
                elif "command":
                    state = handle_command(text)
                elif state == "speech":
                    state = handle_speech(text)
