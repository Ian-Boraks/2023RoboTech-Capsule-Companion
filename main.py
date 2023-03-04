import json
import speech_recognition as sr
from dotenv import load_dotenv
from datetime import datetime
from time import sleep

from lib.chat import init_openai
from lib.recognition import init_recognizer, run_command
from lib.config import setup_config, DAYS_OF_THE_WEEK
from lib.communication import serial_write

config = {}

load_config_from_file = True

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

        if load_config_from_file:
            with open("config.json") as config_json:
                config = json.load(config_json)
        else:
            config = setup_config(source)
        
        print(config)
        
        while True:
            command = True # check button press from serial
            if command:
                run_command(source)

            now = datetime.now()

            if now.date() != today:
                day = config[DAYS_OF_THE_WEEK[now.weekday()]]
                today = now.date()
                state["pills"] = [False for i in day["pills"]]
                state["therapist"] = [False for i in day["therapist"]]
                state["trainer"] = [False for i in day["trainer"]]

            # logic
