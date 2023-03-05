'''
Designed by The Psychedelic Psychologist
Robo-Tech 2023 @ GT
'''

import serial

# TODO: change below serial device to correct one
# device = serial.Serial("/dev/serial0", 9600)
'''
This function will serialize the data in a format our Arduino understands

'''
def serial_write(mode, data):
    op = 0
    if mode == "pills":
        op = 1
    elif mode == "first-aid":
        op = 2
    elif mode == "workout":
        op = 3
    
    b = (op << 6) + data
    
    # NOTE: Uncomment this line and the import
    # device.write(b.to_bytes(1, "big"))
    print(b.to_bytes(1, "big"))