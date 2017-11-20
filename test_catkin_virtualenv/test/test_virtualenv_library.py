import importlib
import unittest


class TestVirtualenv(unittest.TestCase):

    def test_import_wrapt(self):
        importlib.import_module("wrapt")
