from .parser import Parser


class XParser(Parser):
    def __init__(self):
        Parser.__init__(self)
        self.scanner.add_word_characters("_")
        self.define_operators()

    def define_operators(self):
        self.define_prefix_operator("(", self.paren_operator, 0)
        self.define_prefix_operator("+", self.prefix_operator, 100)
        self.define_prefix_operator("-", self.prefix_operator, 100)
        self.define_prefix_operator("!", self.prefix_operator, 100)
        self.define_prefix_operator("++", self.prefix_operator, 100)
        self.define_prefix_operator("--", self.prefix_operator, 100)
        self.define_infix_operator("(", self.apply_operator, 110, "RIGHT")
        self.define_infix_operator("+", self.infix_operator, 80)
        self.define_infix_operator("-", self.infix_operator, 80)
        self.define_infix_operator("++", self.suffix_operator, 100, "RIGHT")
        self.define_infix_operator("--", self.suffix_operator, 100, "RIGHT")
        self.define_infix_operator("*", self.infix_operator, 90)
        self.define_infix_operator("/", self.infix_operator, 90)
        self.define_infix_operator("%", self.infix_operator, 90)
        self.define_infix_operator("<", self.infix_operator, 60)
        self.define_infix_operator("<=", self.infix_operator, 60)
        self.define_infix_operator(">", self.infix_operator, 60)
        self.define_infix_operator(">=", self.infix_operator, 60)
        self.define_infix_operator("==", self.infix_operator, 50)
        self.define_infix_operator("!=", self.infix_operator, 50)
        self.define_infix_operator("&&", self.infix_operator, 30)
        self.define_infix_operator("||", self.infix_operator, 20)
        self.define_infix_operator("?", self.question_mark_colon, 15, "RIGHT")
        self.define_infix_operator("=", self.infix_operator, 10, "RIGHT")
        self.define_infix_operator("+=", self.infix_operator, 10, "RIGHT")
        self.define_infix_operator("-=", self.infix_operator, 10, "RIGHT")
        self.define_infix_operator("*=", self.infix_operator, 10, "RIGHT")
        self.define_infix_operator("/=", self.infix_operator, 10, "RIGHT")
        self.define_infix_operator("%=", self.infix_operator, 10, "RIGHT")

    @staticmethod
    def prefix_operator(parser, op):
        return ["pre" + op, parser.read_e(parser.prefix_properties[op].prec)]

    @staticmethod
    def infix_operator(parser, op, lhs):
        return [op, lhs, parser.read_e(parser.infix_properties[op].prec)]

    @staticmethod
    def suffix_operator(parser, op, lhs):
        return ["post" + op, lhs]

    @staticmethod
    def paren_operator(parser, op):
        exp = parser.read_e(0)
        parser.verify_token(")")
        return exp

    @staticmethod
    def apply_operator(parser, op, lhs):
        exp = ["call", lhs]
        token = parser.next_token()
        if token is ")":
            return exp
        parser.save_token()
        while True:
            exp.append(parser.read_e(0))
            token = parser.next_token()
            if token is ")":
                break
            if token is not ",":
                msg = 'Found: "{}", when expecting "," or ")"'.format(token)
                raise Exception(msg)
        return exp

    @staticmethod
    def question_mark_colon(parser, op, lhs):
        e1 = parser.read_e(0)
        parser.verify_token(":")
        e2 = parser.read_e(parser.infix_properties[op]["prec"])
        return ["?:", lhs, e1, e2]
