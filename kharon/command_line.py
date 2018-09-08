import os
from pkg_resources import resource_filename, Requirement
from shutil import copy
import argparse

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

    #set function corresponding to command
    parser_run.set_defaults(func=makeproject)

    # run function correspondign to command
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