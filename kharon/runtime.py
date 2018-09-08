import pyserial as serial
import inspect
import struct
from functools import wraps

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
    @wraps(cfunc)
    def a(cfunc):
        channel = soul_map[cfunc.__name__]
        message = ''
        for var,type in zip([locals()[arg] for arg in inspect.signature(cfunc).args],cfunc.types):
            message += struct.pack(type.format_string, var)
        ser.write(channel + message + channel)

        return ser.read()

    return a