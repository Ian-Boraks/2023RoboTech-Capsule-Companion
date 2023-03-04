import speech_recognition as sr
from dotenv import load_dotenv

from recognition import start_loop

if __name__ == "__main__":
    load_dotenv()
    start_loop()
