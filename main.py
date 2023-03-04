import threading
import speech_recognition as sr
from dotenv import load_dotenv
from datetime import datetime
from time import sleep

from lib.chat import init_openai
from lib.recognition import init_recognizer, next_state
from lib.setup import setup_week, setup_day
from lib.communication import serial_write

DAYS_OF_THE_WEEK = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
PILLS = {
    "advil": 0,
    "tylenol": 1,
    "xanax": 2
}

config = setup_week()


def speech_recognition():
    with sr.Microphone() as source:
        init_recognizer(source)
        init_openai()
        
        while True:
            next_state(source)

if __name__ == "__main__":
    load_dotenv()

    speech_recognition_thread = threading.Thread(
        target=speech_recognition, name="speech_recognition").start()

    update_day = True
    day = None
    while True:
        if update_day:
            day = setup_day(config["SCHEDULE"][DAYS_OF_THE_WEEK[datetime.today().weekday()]])
            update_day = False

        if len(day) != 0:
            current_task = day.pop(0)
            task_time = current_task[0]

            while task_time != datetime.now().strftime("%H:%M"):
                sleep(1)
            
            s = sum([2**PILLS[x] for x in current_task[2]])
            serial_write(current_task[1], sum([2**PILLS[x] for x in current_task[2]]))
        else:
            update_day = True

        

