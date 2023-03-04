import datetime as dt
from zoneinfo import ZoneInfo
import time_machine
from lib.setup import setup_day
from lib.communication import serial_write
from time import sleep

est_tz = ZoneInfo("America/New_York")
today = dt.datetime.now()

config = {
    "SCHEDULE": {
        "MONDAY": {
            "PILLS": [[0, []]],
            "TRAINER": [[0, []]],
            "THERAPIST": [[0]]
        },
        "TUESDAY": {
            "PILLS": [[0, []]],
            "TRAINER": [[0, []]],
            "THERAPIST": [[0]]
        },
        "WEDNESDAY": {
            "PILLS": [[0, []]],
            "TRAINER": [[0, []]],
            "THERAPIST": [[0]]
        },
        "THURSDAY": {
            "PILLS": [[0, []]],
            "TRAINER": [[0, []]],
            "THERAPIST": [[0]]
        },
        "FRIDAY": {
            "PILLS": [[0, []]],
            "TRAINER": [[0, []]],
            "THERAPIST": [[0]]
        },
        "SATURDAY": {
            "PILLS": [
                [(today + dt.timedelta(minutes=5)).strftime("%H:%M"), ["xanax"]],
                [(today + dt.timedelta(minutes=10)).strftime("%H:%M"), ["tylenol"]],
                [(today + dt.timedelta(hours=1)).strftime("%H:%M"), ["advil"]]
            ],
            "TRAINER": [[0, []]],
            "THERAPIST": [[0]]
        },
        "SUNDAY": {
            "PILLS": [
                [(today + dt.timedelta(hours=1)).strftime("%H:%M"),
                 ["advil", "tylenol", "xanax"]],
                [(today + dt.timedelta(hours=2, minutes=5)).strftime("%H:%M"),
                 ["xanax", "tylenol"]]
            ],
            "TRAINER": [[0, []]],
            "THERAPIST": [[0]]
        }
    }
}

DAYS_OF_THE_WEEK = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
PILLS = {
    "advil": 0,
    "tylenol": 1,
    "xanax": 2
}

def test_scheduler():
    now = dt.datetime.now(tz=est_tz)
    with time_machine.travel(now) as traveller:
        update_day = True
        day = None
        while True:
            if update_day:
                day = setup_day(
                    config["SCHEDULE"][DAYS_OF_THE_WEEK[dt.datetime.today().weekday()]])
                update_day = False

            if len(day) != 0:
                current_task = day.pop(0)
                task_time = current_task[0]

                print(f"The current task is {current_task} on {DAYS_OF_THE_WEEK[dt.datetime.today().weekday()]} with current time at {dt.datetime.now().strftime('%H:%M')}")
                while task_time != dt.datetime.now().strftime("%H:%M"):
                    traveller.shift(dt.timedelta(minutes=1))
                    now = dt.datetime.now(tz=est_tz)

                print(f"It is currently {dt.datetime.now()}")
                serial_write(current_task[1], sum([2**PILLS[x] for x in current_task[2]]))
                print()
            else:
                update_day = True
                traveller.shift(dt.timedelta(days=1))


test_scheduler()
