import threading
import speech_recognition as sr
from dotenv import load_dotenv
from datetime import datetime
from time import sleep

from lib.chat import init_openai
from lib.recognition import init_recognizer, run_command
from lib.config import setup_config, DAYS_OF_THE_WEEK
from lib.communication import serial_write

config = {}

today = None
state = {
    "pills": [],
    "trainer": [],
    "therapist": [],
}


if __name__ == "__main__":
    load_dotenv()

    with sr.Microphone() as source:
        init_recognizer(source)
        init_openai()

        config = setup_config(source)
        
        while True:
            command = True # check button press from serial
            if command:
                run_command()

            now = datetime.now()

            if now.date() != today:
                day = config[DAYS_OF_THE_WEEK[now.weekday()]]
                today = now.date()
                state["pills"] = [False for i in day["pills"]]
                state["therapist"] = [False for i in day["therapist"]]
                state["trainer"] = [False for i in day["trainer"]]

            # logic
