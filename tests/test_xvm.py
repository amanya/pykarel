import unittest

from .vm.vm import VM


class TestXVM(unittest.TestCase):
    def test_run(self):
        vm = VM()
        vm.run("1 == 2")


if __name__ == '__main__':
    unittest.main()
