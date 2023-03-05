'''
Designed by The Psychedelic Psychologist
Robo-Tech 2023 @ GT
'''

import serial

enable_serial = False

if enable_serial:
    device = serial.Serial("/dev/cu.usbmodem144401", 9600)

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
    
    print(b.to_bytes(1, "big"))
    if enable_serial:
        device.write(b.to_bytes(1, "big"))

def check_button():
    if enable_serial:
        if device.in_waiting > 0:
            device.read_all()
            return True
    return False
