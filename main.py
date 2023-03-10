'''
Designed by The Psychedelic Psychologist
RoboTech 2023 @ GT
'''

import json
import speech_recognition as sr
import threading
from dotenv import load_dotenv
from datetime import datetime, timedelta
from time import sleep

from lib.chat import init_openai
from lib.recognition import init_recognizer, run_command, run_therapy
from lib.config import setup_config, DAYS_OF_THE_WEEK
from lib.comms import check_button, serial_write
from lib.speech import init_google, say
from lib.video import play_video

config = {}

load_config_from_file = True

today = None
queue = []

prev_button = False

def setup_tasks_for_day(day):
    for task in day["pills"]:
        temp = task.copy()
        temp.insert(1, "pills")
        queue.append(temp)
        close_task = temp.copy()
        close_task[0] = (datetime.strptime(temp[0], "%H:%M") + timedelta(minutes=5)).strftime("%H:%M")
        close_task[2] = []
        queue.append(close_task)

    
    if len(day["therapist"]) > 0:
        queue.append([day["therapist"], "therapist"])
    if len(day["trainer"]) > 0:
        queue.append([day["trainer"], "trainer"])
    queue.sort()


def main():
    global config, today
    sleep(7)

    with sr.Microphone() as source:
        init_recognizer(source)
        init_openai()
        init_google()

        sleep(1.5)

        if load_config_from_file:
            with open("config.json") as config_json:
                config = json.load(config_json)
        else:
            config = setup_config(source)
        
        while True:
            button = check_button()
            if button and not prev_button: # rising edge
                run_command(source)
            prev_button = button

            now = datetime.now()
            if now.date() != today:
                day = config["schedule"][DAYS_OF_THE_WEEK[now.weekday()]]
                today = now.date()
                setup_tasks_for_day(day)
                print("Setup tasks for", DAYS_OF_THE_WEEK[now.weekday()])
                print(queue)

            # logic
            while len(queue) != 0:
                if queue[0][0] <= datetime.now().strftime("%H:%M"):
                    current_task = queue.pop(0)
                    if current_task[1] == "pills":
                        if len(current_task[2]) > 0:
                            say(f"It's time to take your {' and '.join(current_task[2])}")
                        bit_array = [1 << config["pills"][pill] for pill in current_task[2]]
                        serial_write("pills", sum(bit_array))
                        sleep(10)
                    elif current_task[1] == "therapist":
                        run_therapy(source, current_task[0], first_time=True)
                    elif current_task[1] == "trainer":
                        continue
                else:
                    break


if __name__ == "__main__":
    load_dotenv()

    threading.Thread(target=main).start()

    play_video()
    