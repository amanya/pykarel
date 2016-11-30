import unittest

from scanner.token_scanner import TokenScanner


class TestTokenScanner(unittest.TestCase):
    def test_run(self):
        scanner = TokenScanner("1+112")
        while scanner.has_more_tokens():
            print(scanner.next_token())
