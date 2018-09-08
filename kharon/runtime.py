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


def register(device):
    for cfunc in device.cfuncs:
        device.__dict__[cfunc.__name__] = wrap(cfunc)


def wrap(cfunc):
    @wraps(cfunc)
    def a(cfunc):
        channel = soul_map[cfunc.__name__]
        message = []
        message_format = ''
        for var, type in zip([locals()[arg] for arg in inspect.signature(cfunc).args], cfunc.types):
            message += var
            message_format = type.format_string

        to_send = bytes.fromhex(channel)
        to_send += struct.pack('>h', len(message))
        to_send += str.encode(message)
        ser.write(to_send)

        return ser.read()

    return a
