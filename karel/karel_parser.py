from ..parser.xparser import XParser
from ..scanner.token_scanner import TokenScanner


def if_statement(parser):
    parser.verify_token("(")
    exp = parser.read_predicate()
    parser.verify_token(")")
    s1 = parser.read_statement()
    token = parser.next_token()
    if token == "else":
        return ["if", exp, s1, parser.read_statement()]
    else:
        parser.save_token(token)
        return ["if", exp, s1]


def while_statement(parser):
    parser.verify_token("(")
    exp = parser.read_predicate()
    parser.verify_token(")")
    return ["while", exp, parser.read_statement()]


def repeat_statement(parser):
    parser.verify_token("(")
    token = parser.next_token()
    if TokenScanner.get_token_type(token) is not TokenScanner.NUMBER:
        raise Exception("The repeat statement requires an integer on line {}".format(parser.chars_to_lines()))
    parser.verify_token(")")
    return ["repeat", TokenScanner.get_number(token), parser.read_statement()]


class KarelParser(XParser):
    statement_forms = {}

    def __init__(self):
        XParser.__init__(self)
        self.scanner.add_word_characters("_")
        self.operators = {}
        self.define_operators()
        self.statement_forms = {
            "if": if_statement,
            "while": while_statement,
            "repeat": repeat_statement,
        }

    def define_operators(self):
        self.define_prefix_operator("(", self.paren_operator, 0)
        self.define_prefix_operator("!", self.prefix_operator, 100)
        self.define_infix_operator("(", self.apply_operator, 110, "RIGHT")
        self.define_infix_operator("&&", self.infix_operator, 30)
        self.define_infix_operator("||", self.infix_operator, 20)

    def chars_to_lines(self):
        lines = self.scanner.buffer.split("\n")
        cnt = 0
        for n in range(0, len(lines)):
            cnt += len(lines[n])
            if cnt >= self.scanner.cp:
                return n
        return 0

    def read_function(self):
        self.verify_token("function")
        name = self.next_token()
        if not self.scanner.is_valid_identifier(name):
            raise Exception('"{}" is not a legal function name on line {}'.format(name, self.chars_to_lines()))
        self.verify_token("(")
        self.verify_token(")")
        self.verify_token("{")
        self.save_token("{")
        return ["function", name, self.read_statement()]

    def read_statement(self):
        token = self.next_token()
        if token is "{":
            block = ["block"]
            while True:
                token = self.next_token()
                if token is "}":
                    break
                self.save_token(token)
                stmt = self.read_statement()
                block.append(stmt)
            return block
        prop = KarelParser.statement_forms.get(token, None)
        if prop:
            return prop(self)
        self.verify_token("(")
        self.verify_token(")")
        self.verify_token(";")
        return ["stmt", ["call", token]]

    def read_predicate(self):
        return self.read_e(0)
