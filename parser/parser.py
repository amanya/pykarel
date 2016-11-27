from ..scanner.token_scanner import TokenScanner


class Parser:
    def __init__(self):
        self.scanner = TokenScanner()
        self.scanner.ignore_whitespace = True
        self.scanner.ignore_comments = True
        self.scanner.scan_numbers = True
        self.scanner.scan_strings = True
        self.prefix_properties = {}
        self.infix_properties = {}

    def parse(self):
        exp = self.read_e(0)
        token = self.next_token()
        if token is not "":
            raise Exception('Unexpected token "{}"'.format(token))
        return exp

    def read_e(self, prec):
        if not prec:
            prec = 0
        exp = self.read_t()
        token = self.next_token()
        while self.takes_precedence(token, prec):
            prop = self.infix_properties[token]
            exp = prop["action"](self, token, exp)
            token = self.next_token()
        self.save_token(token)
        return exp

    def read_t(self):
        token = self.next_token()
        token_type = TokenScanner.get_token_type(token)
        if token_type == TokenScanner.EOF:
            raise Exception("Unexpected end of line")
        elif token_type in [TokenScanner.WORD, TokenScanner.OPERATOR]:
            prop = self.prefix_properties.get(token, None)
            if prop:
                return prop.action(self, token)
        return token

    def define_prefix_operator(self, op, fn, prec=0):
        self.prefix_properties[op] = {"prec": prec, "assoc": "LEFT", "action": fn}
        if not self.scanner.is_valid_identifier(op[0]):
            self.scanner.define_operator(op)

    def define_infix_operator(self, op, fn, prec=0, assoc="LEFT"):
        self.infix_properties[op] = {"prec": prec, "assoc": assoc, "action": fn}
        if not self.scanner.is_valid_identifier(op[0]):
            self.scanner.define_operator(op)

    def set_input(self, s):
        self.scanner.set_input(s)

    def next_token(self):
        return self.scanner.next_token()

    def save_token(self, token):
        self.scanner.save_token(token)

    def verify_token(self, expected):
        return self.scanner.verify_token(expected)

    def takes_precedence(self, token, prec):
        token_type = TokenScanner.get_token_type(token)
        if token_type in [TokenScanner.WORD, TokenScanner.OPERATOR]:
            prop = self.infix_properties.get(token, None)
            if not prop:
                return False
            new_prec = prop["prec"]
            if new_prec == prec:
                return prop["assoc"] == "RIGHT"
            return new_prec > prec
        return False

    def unparse(self, exp):
        if type(exp) is list:
            s = "("
            for i in range(0, len(exp)):
                if i > 0:
                    s += " "
                s += self.unparse(exp[i])
            return s + ")"
        return exp

    def __str__(self):
        return str(type(self)) + "(...)"
