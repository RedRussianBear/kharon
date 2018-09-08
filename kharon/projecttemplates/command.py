import argparse
import pyserial as serial
from master import main

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
parser_run.set_defaults(func=main())

# create the parser for the "ferrysouls" command
parser_ferrysouls = subparsers.add_parser('ferrysouls', help='')
parser_ferrysouls.set_defaults(func=ferrysouls())

args = parser.parse_args()
args.func(args)