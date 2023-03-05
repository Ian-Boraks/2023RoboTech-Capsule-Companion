'''
Designed by The Psychedelic Psychologist
Robo-Tech 2023 @ GT
'''

import datetime as dt
from zoneinfo import ZoneInfo
import time_machine
from lib.comms import serial_write
from lib.config import gen_empty_config, DAYS_OF_THE_WEEK

est_tz = ZoneInfo("America/New_York")
today = dt.datetime.now()

config = gen_empty_config()

PILLS = {
    "advil": 0,
    "tylenol": 1,
    "xanax": 2
}

def setup_day(day_of_week):
    '''
    day_of_week =  
         "monday" : {
            "pills" : [[0, []]],
            "trainer": [[0, []]],
             "therapist" : [[0]]
         } 
    '''
    t = []
    for i in day_of_week["pills"]:
        t.append([i[0], "pills", i[1]])
    return t

def test_scheduler():
    config["schedule"]["saturday"] = {
        "pills": [
            [(today + dt.timedelta(minutes=5)).strftime("%H:%M"), ["xanax"]],
            [(today + dt.timedelta(minutes=10)).strftime("%H:%M"), ["tylenol"]],
            [(today + dt.timedelta(hours=1)).strftime("%H:%M"), ["advil"]]
        ],
        "trainer": [[0, []]],
        "therapist": [[0]]
    }
    config["schedule"]["sunday"] = {
        "pills": [
            [(today + dt.timedelta(hours=1)).strftime("%H:%M"),
                ["advil", "tylenol", "xanax"]],
            [(today + dt.timedelta(hours=2, minutes=5)).strftime("%H:%M"),
                ["xanax", "tylenol"]]
        ],
        "trainer": [[0, []]],
        "therapist": [[0]]
    }

    now = dt.datetime.now(tz=est_tz)
    with time_machine.travel(now) as traveller:
        update_day = True
        day = None
        while True:
            if update_day:
                day = setup_day(
                    config["schedule"][DAYS_OF_THE_WEEK[dt.datetime.today().weekday()]])
                update_day = False

            if len(day) != 0:
                current_task = day.pop(0)
                task_time = current_task[0]

                print(f"The current task is {current_task} on {DAYS_OF_THE_WEEK[dt.datetime.today().weekday()]} with current time at {dt.datetime.now().strftime('%H:%M')}")
                while task_time != dt.datetime.now().strftime("%H:%M"):
                    traveller.shift(dt.timedelta(minutes=1))
                    now = dt.datetime.now(tz=est_tz)

                print(f"It is currently {dt.datetime.now()}")
                serial_write(current_task[1], sum([1 << PILLS[x] for x in current_task[2]]))
                print()
            else:
                update_day = True
                traveller.shift(dt.timedelta(days=1))


test_scheduler()
