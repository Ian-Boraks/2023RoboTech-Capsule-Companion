import speech_recognition as sr
import gtts
from io import BytesIO 
from pydub import AudioSegment
from pydub.playback import play
import whisper
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

model = whisper.load_model("small.en")

def listen_and_recognize_whisper(r: sr.Recognizer, source, from_code: str, beep=False, timeout=5):
    if beep:
        afile = AudioSegment.from_wav("beep.wav")
        play(afile)
    print("Listening...")
    audio = r.listen(source)
    with open("temp.wav", "wb") as f:
        f.write(audio.get_wav_data())
        f.flush()
        print("Recognizing...")
        result = model.transcribe(f.name)
        return result['text']

def say(text, to_code):
    tts = gtts.gTTS(text, lang=to_code)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    aud = AudioSegment.from_file(fp, format="mp3")
    play(aud)

def recognize_once(r: sr.Recognizer, source):
    print("Starting...")
    r = setup_microphone()
    text = listen_and_recognize_whisper(r, source, "en", beep=True)
    if text:
        print("Spoken: ", text.lower())
        say(text, "en")

def recognize_command(r: sr.Recognizer, source):
    print("Starting...")
    r = setup_microphone()
    text = listen_and_recognize_whisper(r, source, "en", beep=True)
    print(text)
    if "exit" in text.lower():
        say("exiting", "en")
        sys.exit()
    if "talking" in text.lower():
        say("enter your speech", "en")
        recognize_once(r, source)

def recognize_continuous(r: sr.Recognizer, source):
    print("Starting...")
    while True:
        text = listen_and_recognize_whisper(r, source, "en")
        if "buzz" in text.lower():
            say("yes?", "en")
            recognize_command(r, source)
    
if __name__ == '__main__':
    r = setup_microphone()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Adjusting...")
        recognize_continuous(r, source)
    open("temp.wav", "w").close()