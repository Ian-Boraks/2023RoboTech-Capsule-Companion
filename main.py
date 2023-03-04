import json
import speech_recognition as sr
from dotenv import load_dotenv
from datetime import datetime, timedelta
from time import sleep

from lib.chat import init_openai
from lib.recognition import init_recognizer, run_command
from lib.config import setup_config, DAYS_OF_THE_WEEK
from lib.communication import serial_write

config = {
    "saturday": {
        "pills": [
            ["12:00", "xanax"], 
            ["13:00", "tylenol"],
            ["12:00", "advil"],
            ["13:00", "cocaine"],
            ["11:00", "cocaine"]
        ],
        "therapist": "11:00",
        "trainer": "15:00"
    }
}

load_config_from_file = True

today = None
queue = []

def setup_tasks_for_day(day):
    for task in day["pills"]:
        temp = task.copy()
        temp.insert(1, "pills")
        queue.append(temp)
    
    queue.append([day["therapist"], "therapist"])
    queue.append([day["trainer"], "trainer"])
    queue.sort()
    print(queue)
    


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
            command = False # check button press from serial
            if command:
                run_command(source)

            now = datetime.now()

            if now.date() != today:
                day = config[DAYS_OF_THE_WEEK[now.weekday()]]
                today = now.date()
                print(f"Day: {day}")
                setup_tasks_for_day(day)
                print(f"Queue: {queue}")

            # logic
            while len(queue) != 0:
                current_task = queue.pop(0)
                # perform based on current task

