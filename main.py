import speech_recognition as sr
from dotenv import load_dotenv

from lib.recognition import start_loop

pills = { }

config = setup_week()

day = setup_day(day_of_week)

if __name__ == "__main__":
    load_dotenv()
    start_loop()
