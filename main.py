import json
import speech_recognition as sr
from dotenv import load_dotenv
from datetime import datetime

from lib.chat import init_openai
from lib.recognition import init_recognizer, run_command, run_therapy
from lib.config import setup_config, DAYS_OF_THE_WEEK
from lib.communication import serial_write

config = {}

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
                day = config["schedule"][DAYS_OF_THE_WEEK[now.weekday()]]
                today = now.date()
                setup_tasks_for_day(day)

            # logic
            while len(queue) != 0:
                if queue[0][0] <= datetime.now().strftime("%H:%M"):
                    current_task = queue.pop(0)
                    if current_task[1] == "pills":
                        
                        continue
                    elif current_task[1] == "therpist":
                        run_therapy()
                    elif current_task[2] == "trainer":
                        continue
                else:
                    break
