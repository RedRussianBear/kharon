import argparse

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
parser_run.set_defaults(func=print("run"))

# create the parser for the "makesouls" command
parser_makesouls = subparsers.add_parser('makesouls', help='')
parser_makesouls.set_defaults(func=print("makesouls"))

# create the parser for the "ferrysouls" command
parser_ferrysouls = subparsers.add_parser('ferrysouls', help='')
parser_ferrysouls.set_defaults(func=print("ferrysouls"))