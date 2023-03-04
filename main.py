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


def pill_loop(): # copy-pasted from main loop - change this
    while True:
        continue # temporary


        # use config and state for this

        current_task = day.pop(0)
        task_time = current_task[0]

        while task_time < datetime.now().strftime("%H:%M"):
            sleep(1)
        
        s = sum([2**PILLS[key] for key in current_task[2]])
        task = current_task[1]

        if task == "PILLS":
            serial_write(current_task[1], sum([2**PILLS[key] for key in current_task[2]]))


if __name__ == "__main__":
    load_dotenv()

    with sr.Microphone() as source:
        init_recognizer(source)
        init_openai()

        config = setup_config(source)

        pill_thread = threading.Thread(target=pill_loop, name="pill_loop").start()
        
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
