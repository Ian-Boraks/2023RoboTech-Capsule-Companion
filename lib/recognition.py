import gtts
import speech_recognition as sr
import whisper
import sys
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

r = sr.Recognizer()
model = whisper.load_model("small.en")

def transcribe(source: sr.AudioSource, from_code: str, beep=False):
    if beep:
        afile = AudioSegment.from_wav("assets/beep.wav")
        play(afile)
    print("Listening...")
    audio = r.listen(source)
    with open("temp.wav", "wb") as f:
        f.write(audio.get_wav_data())
        f.flush()
        print("Recognizing...")
        result = model.transcribe(f.name, language=from_code)
        return result["text"]

def say(text: str, to_code: str):
    tts = gtts.gTTS(text, lang=to_code)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    aud = AudioSegment.from_file(fp, format="mp3")
    play(aud)

def recognize_once(source: sr.AudioSource):
    print("Starting...")
    text = transcribe(source, "en", beep=True)
    if text:
        print("Spoken: ", text.lower())
        say(text, "en")

def recognize_command(source: sr.AudioSource):
    print("Starting...")
    text = transcribe(source, "en", beep=True)
    print(text)
    if "exit" in text.lower():
        say("exiting", "en")
        sys.exit()
    if "talking" in text.lower():
        say("enter your speech", "en")
        recognize_once(source)

def recognize_continuous(source: sr.AudioSource):
    print("Starting...")
    while True:
        text = transcribe(source, "en")
        if "buzz" in text.lower():
            say("yes?", "en")
            recognize_command(source)
    
def start_loop():
    with sr.Microphone() as source:
        print("Adjusting...")
        r.adjust_for_ambient_noise(source, duration=1)
        recognize_continuous(source)
