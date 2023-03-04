import gtts
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

lang = "en"

def say(text: str):
    tts = gtts.gTTS(text, lang=lang)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    aud = AudioSegment.from_file(fp, format="mp3")
    play(aud)