import os, sys
import re
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
        return str(arg)

def pdf_file(parser, arg):
    return re.sub(r'([^.]*)(\.|\.p|\.pd|\.pdf)?$', r'\1.pdf', arg, count=1)

def main():
    parser = argparse.ArgumentParser(description=description, epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('file', type=lambda arg: is_valid_file(parser, arg),
            metavar='infile.smd',
            help='Snakemarkdown file to render')

    parser.add_argument('output', type=lambda arg: pdf_file(parser, arg),
            metavar='outfile[.pdf]', nargs='?',
            help='Name of output file. Defaults to name of input file with .pdf extension. The .pdf extension will be appended by default')

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

    if not args.output:
        args.output = re.sub(r'([^.]*)(\..*)?$', r'\1.pdf', args.file, count=1)

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

    log.debug(args.file)
    log.debug(args.output)
