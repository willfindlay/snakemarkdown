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

def parse_args(args):
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
    verbosity.add_argument('-v', '--verbose', dest='log_level', action='store_const',
            const=logging.INFO, default=logging.WARNING,
            help='Log extra information to stderr')
    verbosity.add_argument('-q', '--silent', dest='log_level', action='store_const',
            const=logging.ERROR,
            help='Silence all stderr output')
    verbosity.add_argument('--debug', dest='log_level', action='store_const',
            const=logging.DEBUG,
            help='Log debug output to stderr')

    # Parse arguments
    args = parser.parse_args(args)

    # Fix output file
    if not args.output:
        args.output = re.sub(r'([^.]*)(\..*)?$', r'\1.pdf', args.file, count=1)

    return args

def main():
    args = parse_args(sys.argv[1:])

    # Setup logger
    log = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s - %(levelname)7s: %(message)s')
    formatter.datefmt = '%Y-%m-%d %H:%M:%S'
    log.setLevel(logging.DEBUG)

    # Set up logging to stderr
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(args.log_level)
    formatter = logging.Formatter('%(asctime)s %(levelname)7s: %(message)s')
    formatter.datefmt = '[%H:%M:%S]'
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)


    log = logging.getLogger()

    log.debug(args.file)
    log.debug(args.output)
