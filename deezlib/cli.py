import argparse
import sys

from deezlib import __version__


def build_parser():
    parser = argparse.ArgumentParser(prog="deez", description="Central skills hub.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("version", help="Print the deez version.")
    subparsers.add_parser("python-path", help="Print the interpreter running deez.")
    return parser


def cmd_version(_args):
    print(f"deez {__version__}")
    return 0


def cmd_python_path(_args):
    print(sys.executable)
    return 0


COMMANDS = {"version": cmd_version, "python-path": cmd_python_path}


def main(argv):
    args = build_parser().parse_args(argv)
    return COMMANDS[args.command](args)
