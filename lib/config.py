import speech_recognition as sr

from.communication import serial_write
from .recognition import transcribe
from .speech import say

DAYS_OF_THE_WEEK = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def gen_empty_config():
    config = {"schedule": {}, "pills": []}
    for day in DAYS_OF_THE_WEEK:
        config["schedule"][day] = {
            "pills": [],
            "trainer": [],
            "therapist": [],
        }
    return config

def create_pill_map(source: sr.AudioSource, pills_to_map: set):
    pills = {}
    container = 0
    for pill in pills_to_map:
        pills[pill] = container
        serial_write("pills", 2**container)
        say(f"Please dispense your {pill} into container {container + 1}")
        finished = get_input(source, f"Let me know once you're finished!", split=False)
        if finished.contains("done"):
            serial_write("pills", 0)
            container += 1
            continue
    
    return pills


def get_input(source: sr.AudioSource, prompt: str, split=False):
    text = ""
    while len(text) == 0:
        say(prompt)
        text = transcribe(source)
    if split:
        return [i.lower() for i in text.replace(",", "").split(" ")]
    return text

def setup_config(source: sr.AudioSource):
    config = gen_empty_config()
    pills_to_map = set()
    say("Thank you for choosing BUZZ as your trusted personal helper.")
    say("We are going to start setup now.")

    days = get_input(source, "What days do you take medications?", split=True)
    days = [i for i in days if i in DAYS_OF_THE_WEEK]

    for i in days:
        day = config["schedule"][i]
        
        pills = get_input(source, f"What medication do you take on {i}?", split=True)
        pills = [i for i in pills if i != "and"]
        print(f"{i} pills:", pills)
        for pill in pills:
            # voice recigntion time 
            time = get_input(source, f"What time do you take {pill}?")
            # TODO: Convert time to 24 hour format
            day["pills"].append([time, pill])
            pills_to_map.append(pill)
        # TODO: Return this
        pills = create_pill_map(source, pills_to_map)