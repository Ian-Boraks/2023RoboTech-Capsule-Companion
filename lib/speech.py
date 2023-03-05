'''
Designed by The Psychedelic Psychologist
Robo-Tech 2023 @ GT
'''

from google.cloud import texttospeech
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

lang = "en"

client: texttospeech.TextToSpeechClient
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name="en-US-News-N"
)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3,
    speaking_rate=0.87
)

def init_google():
    global client
    client = texttospeech.TextToSpeechClient()

def say(text: str):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    res = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    fp = BytesIO(res.audio_content)
    audio = AudioSegment.from_file(fp, format="mp3")
    play(audio)
