import unittest

from vm.xvm import XVM

class TestXVM(unittest.TestCase):
    def test_run(self):
        vm = XVM()
        vm.run("1 == 2")
