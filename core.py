import speech_recognition as sr
import gtts
from io import BytesIO 
from pydub import AudioSegment
from pydub.playback import play
import whisper

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

model = whisper.load_model("base.en")

def listen_and_recognize_whisper(r: sr.Recognizer, from_code: str):
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        with open("temp.wav", "wb") as f:
            f.write(audio.get_wav_data())
            f.flush()
            print("Recognizing...")
            result = model.transcribe(f.name)
            print(result['text'])

def recognize_whisper_from_file(r: sr.Recognizer, file_name: str, from_code: str):
    with sr.AudioFile(file_name) as source:
        audio = r.record(source)
        with open("temp.wav", "wb") as f:
            f.write(audio.get_wav_data())
            f.flush()
            result = model.transcribe(f.name)
            print(result['text'])

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
        text = listen_and_recognize_whisper(r, "en")
        if text:
            print("Spoken: ", text)
            say(text, "en")

if __name__ == '__main__':
    main()