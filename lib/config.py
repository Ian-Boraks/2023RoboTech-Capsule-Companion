import re
import speech_recognition as sr

from .recognition import transcribe
from .speech import say

DAYS_OF_THE_WEEK = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def gen_empty_config():
    config = {"schedule": {}}
    for day in DAYS_OF_THE_WEEK:
        config[day] = {
            "pills": [],
            "trainer": [],
            "therapist": [],
        }
    return config

def get_input(source: sr.AudioSource, prompt: str, split=False):
    text = ""
    while len(text) == 0:
        say(prompt)
        text = transcribe(source)
    if split:
        return [i.strip().lower() for i in re.split(",|and|, and", text)]
    return text

def setup_config(source: sr.AudioSource):
    config = gen_empty_config()

    say("Thank you for choosing BUZZ as your trusted personal helper.")
    say("We are going to start setup now.")

    days = get_input(source, "What days do you take medications?", split=True)

    for i in days:
        day = config["schedule"][i]
        
        pills = get_input(source, f"What medication do you take on {DAYS_OF_THE_WEEK[i]}?", split=True)
        for pill in pills:
            # voice recigntion time 
            time = get_input(f"What time do you take {pill}?")
            # TODO: Convert time to 24 hour format
            day["pills"].append([time, pill])
