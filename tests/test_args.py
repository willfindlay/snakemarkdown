import unittest
import tempfile

from snakemarkdown import parse_args

class TestArgs(unittest.TestCase):

    def setUp(self):
        args = ['test']
        self.args = parse_args(args)

    def test_verbose(self):
        pass
