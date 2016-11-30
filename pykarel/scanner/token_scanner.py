import re

is_digit = re.compile("^\d$")
is_alnum = re.compile("^[a-zA-Z0-9]$")
is_xdigit = re.compile("^[a-fA-F0-9]$")
is_space = re.compile("^\s$")
is_alpha = re.compile("^[a-zA-Z]$")


class TokenScanner:
    MAX_TO_STRING_LENGTH = 20
    EOF = -1
    SEPARATOR = 0
    WORD = 1
    NUMBER = 2
    STRING = 3
    OPERATOR = 4

    ignore_whitespace = False
    ignore_comments = False
    scan_numbers = False
    scan_strings = False
    operators = {}
    word_chars = ""

    def __init__(self, input_str=""):
        self.buffer = input_str
        self.length = len(input_str)
        self.cp = 0
        self.saved_characters = []
        self.saved_tokens = []

    def set_input(self, input_str=""):
        self.buffer = input_str
        self.length = len(input_str)
        self.cp = 0
        self.saved_characters = []
        self.saved_tokens = []

    def has_more_tokens(self):
        token = self.next_token()
        self.save_token(token)
        return token is not ""

    def next_token(self):
        if len(self.saved_tokens):
            return self.saved_tokens.pop()
        while True:
            if self.ignore_whitespace:
                self._skip_spaces()
            ch = self._get_char()
            if ch == "":
                return ""
            if ch == "/" and self.ignore_comments:
                ch = self._get_char()
                if ch == "/":
                    while True:
                        ch = self._get_char()
                        if ch == "\n" or ch == "\r" or ch == "":
                            break
                    continue
                elif ch == "*":
                    prev = ""
                    while True:
                        ch = self._get_char()
                        if ch == "" or (prev == "*" and ch == "/"):
                            break
                        prev = ch
                    continue
                self._save_char(ch)
                ch = "/"
            if (ch == '"' or ch == "'") and self.scan_strings:
                self._save_char(ch)
                return self._scan_string()
            if is_digit.match(ch) and self.scan_numbers:
                self._save_char(ch)
                return self._scan_number()
            if self.is_word_character(ch):
                self._save_char(ch)
                return self._scan_word()
            op = ch
            while self._is_operator_prefix(op):
                ch = self._get_char()
                if ch == "":
                    break
                op += ch
            while len(op) > 1 and not self._is_operator(op):
                self._save_char(op[len(op) - 1])
                op = op[0:len(op) - 1]
            return op

    def save_token(self, token):
        self.saved_tokens.append(token)

    def verify_token(self, expected):
        token = self.next_token()
        if token != expected:
            msg = 'Found "{}" when expecting: "{}", on line {}'.format(token, expected, self._chars_to_lines())
            raise Exception(msg)

    def add_word_characters(self, s):
        self.word_chars += s

    def define_operator(self, op):
        self.operators[op] = True

    def get_position(self):
        if len(self.saved_tokens) == 0:
            return self.cp
        if len(self.saved_tokens) == 1:
            return self.cp - len(self.saved_tokens[0])
        msg = 'Internal error: get_position after two saves on line: {}'.format(self._chars_to_lines())
        raise Exception(msg)

    def is_valid_identifier(self, token):
        if len(token) == 0:
            return False
        ch = token[0]
        if not self.is_word_character(ch) or is_digit.match(ch):
            return False
        for ch in token[1:]:
            if not self.is_word_character(ch):
                return False
        return True

    def is_word_character(self, ch):
        return is_alnum.match(ch) or ch in self.word_chars

    @staticmethod
    def get_token_type(token):
        if token == "":
            return TokenScanner.EOF
        ch = token[0]
        if is_space.match(ch):
            return TokenScanner.SEPARATOR
        if ch == '"' or ch == "'":
            return TokenScanner.STRING
        if is_digit.match(ch):
            return TokenScanner.NUMBER
        if is_alpha.match(ch):
            return TokenScanner.WORD
        if ch in TokenScanner.word_chars:
            return TokenScanner.WORD
        return TokenScanner.OPERATOR

    def __str__(self):
        msg = str(type(self))
        if len(self.buffer) < self.MAX_TO_STRING_LENGTH:
            msg += '("{}")'.format(self.buffer)
        else:
            msg += '({} chars)'.format(len(self.buffer))
        return msg

    @staticmethod
    def get_string(token):
        return eval(token)

    @staticmethod
    def get_number(token):
        return eval(token)

    def _get_char(self):
        if len(self.saved_characters) == 0:
            if self.cp >= self.length:
                return ""
            else:
                ret = self.buffer[self.cp]
                self.cp += 1
                return ret
        else:
            self.cp += 1
            return self.saved_characters.pop()

    def _save_char(self, ch):
        self.cp -= 1
        self.saved_characters.append(ch)

    def _skip_spaces(self):
        while True:
            ch = self._get_char()
            if ch == "":
                return
            if not is_space.match(ch):
                self._save_char(ch)
                return

    def _scan_word(self):
        token = ""
        while True:
            ch = self._get_char()
            if ch == "":
                break
            if not self.is_word_character(ch):
                self._save_char(ch)
                break
            token += ch
        return token

    def _scan_number(self):
        INITIAL_STATE = 0
        BEFORE_DECIMAL_POINT = 1
        AFTER_DECIMAL_POINT = 2
        STARTING_EXPONENT = 3
        FOUND_EXPONENT_SIGN = 4
        SCANNING_EXPONENT = 5
        LEADING_ZERO = 6
        SCANNING_HEX = 7
        FINAL_STATE = 8

        token = ""
        state = INITIAL_STATE
        while state is not FINAL_STATE:
            ch = self._get_char()
            xch = "e"
            if state is INITIAL_STATE:
                if ch == "=":
                    state = LEADING_ZERO
                else:
                    state = BEFORE_DECIMAL_POINT
            elif state is BEFORE_DECIMAL_POINT:
                if ch == ".":
                    state = AFTER_DECIMAL_POINT
                elif ch == "E" or ch == "e":
                    state = STARTING_EXPONENT
                    xch = ch
                elif not is_digit.match(ch):
                    self._save_char(ch)
                    state = FINAL_STATE
            elif state is AFTER_DECIMAL_POINT:
                if ch == "E" or ch == "e":
                    state = STARTING_EXPONENT
                    xch = ch
                elif not is_digit.match(ch):
                    self._save_char(ch)
                    state = FINAL_STATE
            elif state is STARTING_EXPONENT:
                if ch == "+" or ch == "-":
                    state = FOUND_EXPONENT_SIGN
                elif is_digit.match(ch):
                    state = SCANNING_EXPONENT
                else:
                    self._save_char(ch)
                    state = FINAL_STATE
            elif state is FOUND_EXPONENT_SIGN:
                if is_digit.match(ch):
                    state = SCANNING_EXPONENT
                else:
                    self._save_char(ch)
                    self._save_char(xch)
                    state = FINAL_STATE
            elif state is SCANNING_EXPONENT:
                if not is_digit.match(ch):
                    self._save_char(ch)
                    state = FINAL_STATE
            elif state is LEADING_ZERO:
                if ch == 'x' or ch == 'X':
                    state = SCANNING_HEX
                elif ch == ".":
                    state = AFTER_DECIMAL_POINT
                elif ch == "E" or ch == "e":
                    state = STARTING_EXPONENT
                elif not is_digit.match(ch):
                    self._save_char(ch)
                    state = FINAL_STATE
            elif state is SCANNING_HEX:
                pass
            else:
                state = FINAL_STATE

            if state is not FINAL_STATE:
                token += ch
        return token

    def _scan_string(self):
        token = ""
        delim = self._get_char()
        token += delim
        while True:
            ch = self._get_char()
            if ch == "":
                raise Exception("Unterminated string on line {}".format(self._chars_to_lines()))
            elif ch == delim:
                break
            elif ch == "\\":
                token += self._scan_escape_character()
            else:
                token += ch
        return token + delim

    def _scan_escape_character(self):
        s = "\\"
        ch = self._get_char()
        s += ch
        if is_digit.match(ch) or ch == 'x' or ch == 'u':
            is_hex = not is_digit.match(ch)
            while True:
                ch = self._get_char()
                if is_hex and is_xdigit.match(ch) or not is_digit.match(ch):
                    break
                s += ch
            self._save_char(ch)
        return s

    def _is_operator(self, op):
        return op in self.operators

    def _is_operator_prefix(self, op):
        for operator in self.operators.keys():
            if operator.startswith(op):
                return True
        return False

    def _chars_to_lines(self):
        lines = self.buffer.split("\n")
        cnt = 0
        for n in range(0, len(lines)):
            cnt += len(lines[n])
            if cnt >= self.cp:
                return n
        return 0
