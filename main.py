import speech_recognition as sr
from dotenv import load_dotenv

from lib.chat import init_openai
from lib.recognition import init_recognizer, next_state

pills = { }

config = setup_week()

day = setup_day(day_of_week)

if __name__ == "__main__":
    load_dotenv()

    with sr.Microphone() as source:
        init_recognizer(source)
        init_openai()
        
        while True:
            next_state(source)
