import os
from pkg_resources import resource_filename, Requirement
from shutil import copy
import argparse
import serial
import serial.tools.list_ports



def kharon():
    parser = argparse.ArgumentParser(description='Create a new Kharon Project')
    parser.add_argument('command', action='store_true', help='The name of the new directory')
    subparsers = parser.add_subparsers(help='sub-command help')

    # create the parser for the "makeproject" command
    parser_run = subparsers.add_parser('makeproject', help='Makes a new Kharon project.')
    parser_run.add_argument(
        'name',
        type=str,
        help='The name of the new project'
    )

    # set function corresponding to command
    parser_run.set_defaults(func=makeproject)

    # run function corresponding to command
    args = parser.parse_args()
    args.func(args)


def makeproject(args):
    template_path = resource_filename(Requirement.parse("kharon"), "kharon/projecttemplates/")
    template_files = os.listdir(template_path)

    os.mkdir(os.getcwd() + "/" + args.name)

    for filename in template_files:
        if not filename in ['__init__.py', '__pycache__']:
            print(template_path + filename)
            copy(template_path + filename, os.getcwd() + "/" + args.name + "/" + filename)


def upload(file_path, arduino_type="", to_search="Arduino"):
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
        str = " ".join(("arduino", "--port", arduino_ports[0].device, "--upload", file_path))
        print(str)
        status = os.system(str)
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
