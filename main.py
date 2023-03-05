'''
Designed by The Psychedelic Psychiatrist
Robo-Tech 2023 @ GT
'''

import json
import speech_recognition as sr
from dotenv import load_dotenv
from datetime import datetime

from lib.chat import init_openai
from lib.recognition import init_recognizer, run_command, run_therapy
from lib.config import setup_config, DAYS_OF_THE_WEEK
from lib.communication import serial_write

config = {}

load_config_from_file = False

today = None
queue = []

def setup_tasks_for_day(day):
    for task in day["pills"]:
        temp = task.copy()
        temp.insert(1, "pills")
        queue.append(temp)
    
    if len(day["therapist"]) > 0:
        queue.append([day["therapist"], "therapist"])
    if len(day["trainer"]) > 0:
        queue.append([day["trainer"], "trainer"])
    queue.sort()


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
        
        print(json.dumps(config, indent=2))
        
        while True:
            command = False # check button press from serial
            if command:
                run_command(source)

            now = datetime.now()

            if now.date() != today:
                day = config["schedule"][DAYS_OF_THE_WEEK[now.weekday()]]
                today = now.date()
                setup_tasks_for_day(day)
                print("Setup tasks for", DAYS_OF_THE_WEEK[now.weekday()])

            # logic
            while len(queue) != 0:
                if queue[0][0] <= datetime.now().strftime("%H:%M"):
                    current_task = queue.pop(0)
                    if current_task[1] == "pills":
                        bit_array = [1 << config['pills'][pill] for pill in current_task[2]]
                        serial_write("pills", sum(bit_array))
                    elif current_task[1] == "therapist":
                        run_therapy(source, current_task[0])
                    elif current_task[1] == "trainer":
                        continue
                else:
                    break
