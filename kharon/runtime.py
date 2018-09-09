import serial
import inspect
import struct
from functools import wraps
from .ferry import get_functions

# Placeholder JSON
soul_map = {"device_name": "AB23"}

# Placeholder settings
DEVICE_LOCATION = "/DEV/TTY1"
BAUD_RATE = 9600

ser = serial.Serial(DEVICE_LOCATION, BAUD_RATE)


def register(device):
    for func in get_functions(device):
        device.__dict__[func[1].__name__] = wrap(func[1])


def wrap(func):
    @wraps(func)
    def a(funky):
        channel = soul_map[func.__name__]
        message = []
        message_format = ''
        for var, type in zip([locals()[arg] for arg in inspect.signature(func).args], func.types):
            message += var
            message_format = type.format_string

        to_send = bytes.fromhex(channel)
        to_send += struct.pack('>h', len(message))
        to_send += str.encode(message)
        ser.write(to_send)

        return ser.read()

    return a
