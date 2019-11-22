import unittest
import tempfile
import logging

from snakemarkdown import parse_args

class TestArgs(unittest.TestCase):
    def setUp(self):
        self.smd_file = tempfile.NamedTemporaryFile()

    def tearDown(self):
        pass

    def test_verbosity(self):
        # Normal
        args = [self.smd_file.name]
        args = parse_args(args)
        self.assertEqual(args.log_level, logging.WARNING)

        # Verbose
        args = [self.smd_file.name, '-v']
        args = parse_args(args)
        self.assertEqual(args.log_level, logging.INFO)

        # Debug
        args = [self.smd_file.name, '--debug']
        args = parse_args(args)
        self.assertEqual(args.log_level, logging.DEBUG)

        # Silent
        args = [self.smd_file.name, '-q']
        args = parse_args(args)
        self.assertEqual(args.log_level, logging.ERROR)

    def test_infile(self):
        args = [self.smd_file.name]
        args = parse_args(args)
        self.assertEqual(args.file, self.smd_file.name)

    def test_outfile(self):
        # Default
        args = [self.smd_file.name]
        args = parse_args(args)
        self.assertEqual(args.output, f'{self.smd_file.name}.pdf')

        # Custom
        args = [self.smd_file.name, 'testificate']
        args = parse_args(args)
        self.assertEqual(args.output, f'testificate.pdf')

        args = [self.smd_file.name, 'testificate.pdf']
        args = parse_args(args)
        self.assertEqual(args.output, f'testificate.pdf')

        args = [self.smd_file.name, 'testificate.pd.pdf']
        args = parse_args(args)
        self.assertEqual(args.output, f'testificate.pd.pdf')

        args = [self.smd_file.name, 'testificate.f.pdf']
        args = parse_args(args)
        self.assertEqual(args.output, f'testificate.f.pdf')

        args = [self.smd_file.name, 'testificate.']
        args = parse_args(args)
        self.assertEqual(args.output, f'testificate.pdf')

        args = [self.smd_file.name, 'testificate.pd']
        args = parse_args(args)
        self.assertEqual(args.output, f'testificate.pdf')
