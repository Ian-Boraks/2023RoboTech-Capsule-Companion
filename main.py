import speech_recognition as sr
from dotenv import load_dotenv

from lib.recognition import start_loop

pills = { }

day = []

config = {
    "SCHEDULE" : {
        "MONDAY" : {
            "PILLS" : [[0, []]],
            "TRAINER": [[0, []]],
            "THERAPIST" : [[0]]
        },
        "TUESDAY" : {
            "PILLS" : [[0, []]],
            "TRAINER": [[0, []]],
            "THERAPIST" : [[0]]
        },
        "WEDNESDAY" : {
            "PILLS" : [[0, []]],
            "TRAINER": [[0, []]],
            "THERAPIST" : [[0]]
        },
        "THURSDAY" : {
            "PILLS" : [[0, []]],
            "TRAINER": [[0, []]],
            "THERAPIST" : [[0]]
        },
        "FRIDAY" : {
            "PILLS" : [[0, []]],
            "TRAINER": [[0, []]],
            "THERAPIST" : [[0]]
        },
        "SATURDAY" : {
            "PILLS" : [[0, []]],
            "TRAINER": [[0, []]],
            "THERAPIST" : [[0]]
        },
        "SUNDAY" : {
            "PILLS" : [[0, []]],
            "TRAINER": [[0, []]],
            "THERAPIST" : [[0]]
        }
    }
}

if __name__ == "__main__":
    load_dotenv()
    start_loop()
