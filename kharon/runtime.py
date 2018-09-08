import pyserial as serial

# Placeholder JSON
soul_map = {"device_name": "AB23"}

# Placeholder settings
DEVICE_LOCATION = "/DEV/TTY1"
BAUD_RATE = 9600

ser = serial.Serial(DEVICE_LOCATION, BAUD_RATE)


def reigster(device):
    for cfunc in device.cfuncs:
        device.__dict__[cfunc.__name__] = wrap(cfunc)


def wrap(cfunc):
    def a(cfunc):
        channel = soul_map[cfunc.__name__]
        ser.write(channel+  +channel)