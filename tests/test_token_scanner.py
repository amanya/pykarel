import unittest

from pykarel.scanner.token_scanner import TokenScanner


class TestTokenScanner(unittest.TestCase):
    def test_run(self):
        tokens = []
        scanner = TokenScanner("1+112")
        while scanner.has_more_tokens():
            tokens.append(scanner.next_token())
        self.assertEqual(tokens, ["1", "+", "112"])

if __name__ == '__main__':
    unittest.main()
