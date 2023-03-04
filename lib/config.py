import re
import speech_recognition as sr
from datetime import time

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

def create_pill_map(source: sr.AudioSource, pills_to_map: set):
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

def setup_config(source: sr.AudioSource):
    config = gen_empty_config()
    say("Thank you for choosing BUZZ as your trusted personal helper.")
    say("We are going to start setup now.")

    days = get_input(source, "What days do you take medications?", split=True)
    days = [i for i in days if i in DAYS_OF_THE_WEEK]

    pills_to_map = set()
    for i in days:
        day = config["schedule"][i]
        
        pills = get_input(source, f"What medication do you take on {i}?", split=True)
        pills = [j for j in pills if j != "and"]
        for pill in pills:
            timelist = []
            while len(timelist) < 4:
                timelist = get_input(source, f"What time do you take {pill}?")
                timelist = [int(j) for j in timelist if j.isdigit()]
            hour = timelist[0] * 10 + timelist[1]
            minute = timelist[2] * 10 + timelist[3]
            
            day["pills"].append([f"{hour}:{minute}", pill])
            pills_to_map.add(pill)
        
    config["pills"] = create_pill_map(source, pills_to_map)
