# Code Directory Structure and Explanation

```tree
├── CODE.md
├── README.md
├── assets
│   ├── beep.wav
│   ├── idle.mp4
│   └── wave.mp4
├── baymax
│   └── baymax.ino
├── config.json
├── example_transcripts.txt
├── lib
│   ├── chat.py
│   ├── communication.py
│   ├── config.py
│   ├── recognition.py
│   ├── speech.py
│   └── video.py
├── main.py
├── requirements.txt
├── scheduler_tests.py
```

`main.py`

The main starting point of our program. Run this when running the program, it connects all the various interfaces of our application together. It relies on a Queue to determine which task to execute next such as dispensing pills or entering a therapy session.

`baymax/baymax.ino`

Microcontroller code to control the servos and the drawers for the pill dispenser. We had to define our own custom data format. It expects to recieve a byte with the first two bits representing the opcode and the last 6 bits representing the data for the opcode.

The defined opcodes are:

`00` - Reset state

`01` - Dispense Pills

For the Dispense Pills opcode, each bit in the data part maps to a pill container.

`config.json`

A potential permanent storage medium for the configuration for certain users to be loaded into the program on startup

`example_transcripts.txt`

A list of potential possible conversations possible with the therapy bot. Shows multiple different scenarios and how the bot will respond

`lib/`

Directory containing all the library code and helper functions that the bot and pill dispenser to function properly

`lib/chat.py`

Crucial for communication with OpenAI and their Chat Completion API. Significant amount of time went into trying to engineer the optimum prompt to help the therapy bot to be as helpful as possible

`lib/communication.py`

Responsible for serializing pill dispenser data into binary to send to the arduino over serial communications. The serial file will have to be updated every time (need to automatically update in the future)

`lib/config.py`

Helps create the config structure and runs through the initial setup process

`lib/recognition.py`

Uses various APIs like the Whisper API to provide the therapy bot functionality as well as voice recognition

`lib/speech.py`

Relies on the Google Cloud Text to Speech API to convert the OpenAI Chat Completion API text into speech for the user to provide a more enriched therapy experience

`lib/video.py`

Code to display the hologram on the screen and update the models

`assets/`

Contains the video and sound files being used throughout the project.