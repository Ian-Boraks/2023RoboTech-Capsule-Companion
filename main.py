import speech_recognition as sr
from dotenv import load_dotenv

from lib.recognition import start_loop

pills = { }

config = {
    "PILLS": {
        "MONDAY": [
            0, []
        ],
        "TUESDAY": [
            0, []
        ],
        "WEDNESDAY": [
            0, []
        ],
        "THURSDAY": [
            0, []
        ],
        "FRIDAY": [
            0, []
        ],
        "SATURDAY": [
            0, []
        ],
        "SUNDAY": [
            0, []
        ]
    }
}

if __name__ == "__main__":
    load_dotenv()
    start_loop()
