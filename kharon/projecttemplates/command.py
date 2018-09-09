import argparse
import serial
import serial.tools.list_ports
import os
import inspect
import struct
import json
from functools import wraps

from kharon import ferry
from kharon.ferry import get_functions

from .master import main
from .devices import Device
from .settings import BAUD_RATE


def run_device(to_search="Arduino"):
    soul_map = json.loads('soul_map.json')
    arduino_ports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if to_search in p.description
    ]
    device_location = arduino_ports[0]

    ser = serial.Serial(device_location, BAUD_RATE)

    def register(device):
        for func in get_functions(device):
            device.__dict__[func[1].__name__] = wrap(func[1])

    def wrap(func):
        @wraps(func)
        def a(funky):
            channel = soul_map[func.__name__]
            message = []
            message_format = ''
            for var, func_type in zip([locals()[arg] for arg in inspect.signature(func).args], func.types):
                message += var
                message_format = func_type.format_string

            to_send = bytes.fromhex(channel)
            to_send += struct.pack('>h', len(message))
            to_send += str.encode(message)
            ser.write(to_send)

            return ser.read()

        return a

    register(Device)
    main()


parser = argparse.ArgumentParser(description='A CLI for Kharon Commands.')
parser.add_argument('command', action='store_true', help='foo help')
subparsers = parser.add_subparsers(help='sub-command help')

# create the parser for the "run" command
parser_run = subparsers.add_parser('run', help='Transpiles, compiles, and uploads code to relevant devices')
parser_run.add_argument(
    '--serial',
    '-s',
    type=str,
    help='optional argument for what serial port is being used [e.g. /dev/TTY0, /com3, etc.]'
)
parser_run.set_defaults(func=run_device)

# create the parser for the "ferry_souls" command
parser_ferry_souls = subparsers.add_parser('ferry_souls', help='')


def ferry_souls():
    ferry.assemble(Device)
    compile_and_upload('souls.ino')


parser_ferry_souls.set_defaults(func=ferry_souls)

args = parser.parse_args()
args.func(args)


def compile_and_upload(file_path, arduino_type="", to_search="Arduino"):
    arduino_ports = [
        p
        for p in serial.tools.list_ports.comports()
        if to_search in p.description
    ]

    if not arduino_ports:
        raise IOError("No Arduino detected")
    if len(arduino_ports) > 1:
        print("Use of multiple arduinos is not supported at this time. Apologies for any inconvenience.")
    # Maybe ask user which one they want?

    # This might not work, we'll likely have to debug when rolling hardware out
    if arduino_type:
        status = os.system(
            " ".join(("arduino", "--board", arduino_type, "--port", arduino_ports[0].device, "--upload", file_path)))
    else:
        string = " ".join(("arduino", "--port", arduino_ports[0].device, "--upload", file_path))
        print(string)
        status = os.system(string)
    if status == 1:
        print("Compilation/Upload Error")
    elif status == 2:
        print("File not found")
    elif status == 3:
        print("Invalid argument")
    elif status == 4:
        print("oh no")
    elif status == 0:
        print("yay")
    else:
        print(status)
