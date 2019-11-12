#! /usr/bin/env python3

import os, sys
import argparse
import logging

description = """
"""

epilog = """
"""

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error(f'No such file or directory: {arg}')
    elif not os.path.isfile(arg):
        parser.error(f'{arg} is not a file')
    else:
        return os.path.realpath(str(arg))

def main():
    parser = argparse.ArgumentParser(description=description, epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('file', type=lambda arg: is_valid_file(parser, arg),
            metavar='file.smd',
            help='Snakemarkdown file to render')

    # Which intermediate files to keep
    parser.add_argument('-k', '--keep', action='append', choices=['markdown', 'tex'],
            help='Which intermediate files to keep')

    # How verbose does the user want the program to be?
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument('-v', '--verbose', dest='verbose', action='store_true',
            help='Log extra information to stderr')
    verbosity.add_argument('-q', '--silent', dest='silent', action='store_true',
            help='Silence all stderr output')
    verbosity.add_argument('--debug', dest='debug', action='store_true',
            help='Log debug output to stderr')

    # Parse arguments
    args = parser.parse_args()

    # Setup logger
    log = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s - %(levelname)7s: %(message)s')
    formatter.datefmt = '%Y-%m-%d %H:%M:%S'
    log.setLevel(logging.DEBUG)

    # Set up logging to stderr
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO if args.verbose else
            logging.ERROR if args.silent else logging.DEBUG if args.debug
            else logging.WARNING)
    formatter = logging.Formatter('%(asctime)s %(levelname)7s: %(message)s')
    formatter.datefmt = '[%H:%M:%S]'
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)

if __name__ == "__main__":
    main()
