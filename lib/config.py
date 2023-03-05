'''
Designed by The Psychedelic Psychiatrist
Robo-Tech 2023 @ GT
'''

import re
import speech_recognition as sr

from .communication import serial_write
from .recognition import transcribe
from .speech import say

DAYS_OF_THE_WEEK = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def gen_empty_config():
    config = {"schedule": {}, "pills": {}}
    for day in DAYS_OF_THE_WEEK:
        config["schedule"][day] = {
            "pills": [],
            "trainer": "",
            "therapist": "",
        }
    return config

def create_servo_map(source: sr.AudioSource, pills_to_map: set):
    pills = {}
    container = 0
    for pill in pills_to_map:
        pills[pill] = container
        serial_write("pills", 1 << container)
        say(f"Please dispense your {pill} into container {container + 1}")

        done = ''
        while not ("done" in done or "finished" in done):
            done = get_input(source, f"Let me know once you're finished!")
        serial_write("pills", 0)
        container += 1
    
    return pills


def get_input(source: sr.AudioSource, prompt: str, split=False):
    text = ""
    while len(text) == 0:
        say(prompt)
        text = transcribe(source)
    if split:
        return [i.lower() for i in re.sub("[,.!?]", "", text).split(" ") if len(i) > 0]
    return text

def get_time_input(source: sr.AudioSource, prompt: str):
    digits = []
    while len(digits) < 4:
        digits = get_input(source, prompt)
        digits = [int(i) for i in digits if i.isdigit()]
    hour = min(digits[0] * 10 + digits[1], 23)
    minute = min(digits[2] * 10 + digits[3], 59)
    return f"{hour:02d}:{minute:02d}"

def setup_config(source: sr.AudioSource):
    config = gen_empty_config()
    say("Thank you for choosing BUZZ as your trusted personal helper. We are going to start setup now.")

    days = get_input(source, "What days do you take medications?", split=True)
    days = [i for i in days if i in DAYS_OF_THE_WEEK]

    pill_set = set()
    for i in days:
        time_map = {}
        
        pills = get_input(source, f"What medication do you take on {i}?", split=True)
        pills = [j for j in pills if j != "and" and j != "in"]
        for pill in pills:
            time = get_time_input(source, f"What time do you take {pill}?")

            if time in time_map:
                time_map[time].append(pill)
            else:
                time_map[time] = [pill]
            
            pill_set.add(pill)
        
        for j in time_map:
            config["schedule"][i]["pills"].append([j, time_map[j]])
    
    days = get_input(source, "Moving on. What days would you like a therapy session?", split=True)
    days = [i for i in days if i in DAYS_OF_THE_WEEK]
    for i in days:
        config["schedule"][i]["therapist"] = get_time_input(source, f"What time would you like your session on {i}?")
        
    config["pills"] = create_servo_map(source, pill_set)

    return config
