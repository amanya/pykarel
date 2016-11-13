from vm import *


class XVM(VM):
    def __init__(self):
        VM.__init__(self)
        self.init_operators()

    def init_operators(self):
        self.define_operator(PrefixOp("+", lambda x: x))
        self.define_operator(PrefixOp("-", lambda x: -x))
        self.define_operator(PrefixOp("!", lambda x: not x))
        self.define_operator(InfixOp("+", lambda x, y: x + y))
        self.define_operator(InfixOp("-", lambda x, y: x - y))
        self.define_operator(InfixOp("*", lambda x, y: x * y))
        self.define_operator(InfixOp("/", lambda x, y: x / y))
        self.define_operator(InfixOp("%", lambda x, y: x % y))
        self.define_operator(InfixOp("==", lambda x, y: x is y))
        self.define_operator(InfixOp("!=", lambda x, y: x is not y))
        self.define_operator(InfixOp("<", lambda x, y: x < y))
        self.define_operator(InfixOp("<=", lambda x, y: x <= y))
        self.define_operator(InfixOp(">", lambda x, y: x > y))
        self.define_operator(InfixOp(">=", lambda x, y: x >= y))
        self.define_operator(AssignOp("="))
        self.define_operator(AssignOp("+=", lambda x, y: x + y))
        self.define_operator(AssignOp("-=", lambda x, y: x - y))
        self.define_operator(AssignOp("*=", lambda x, y: x * y))
        self.define_operator(AssignOp("/=", lambda x, y: x / y))
        self.define_operator(AssignOp("%=", lambda x, y: x % y))
        self.define_operator(PrefixIncDecOp("++"))
        self.define_operator(PrefixIncDecOp("--"))
        self.define_operator(PostfixIncDecOp("++"))
        self.define_operator(PostfixIncDecOp("--"))
        self.define_operator(ShortCircuitOp("&&"))
        self.define_operator(ShortCircuitOp("||"))
        self.define_operator(QuestionMarkColonOp())
        self.define_operator(CallIns())


class PrefixIncDecOp:
    def __init__(self, name):
        self.name = "pre" + name
        if name is "++":
            self.fn = lambda x: x + 1
        else:
            self.fn = lambda x: x - 1

    def __str__(self):
        return self.name

    def compile(self, vm, exp, code):
        vm.compile(exp[1], code)
        code.push(self)
        code.push(StoreIns(exp[1]))

    def execute(self, vm):
        vm.push(self.fn(vm.pop()))


class PostfixIncDecOp:
    def __init__(self, name):
        self.name = "pre" + name

    def __str__(self):
        return self.name

    def compile(self, vm, exp, code):
        vm.compile(exp[1], code)
        code.push(DupIns())
        code.push(self)
        code.push(StoreIns(exp[1]))
        code.push(PopIns())

    def execute(self, vm):
        vm.push(self.vm(vm.pop()))


class ShortCircuitOp:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def compile(self, vm, exp, code):
        jump_op = JumpIns((self.name is "&&") and "jumpf" or "jumpt")
        vm.compile(exp[1], code)
        code.push(DupIns())
        code.push(jump_op)
        code.push(PopIns())
        vm.compile(exp[2], code)
        jump_op.set_traget(code.length)


class QuestionMarkColonOp:
    def __init__(self):
        self.name = "?:"

    def __src__(self):
        return self.name

    def compile(self, vm, exp, code):
        jump1 = JumpIns("jumpf")
        jump2 = JumpIns("jump")
        vm.compile(exp[1], code)
        code.push(jump1)
        vm.compile(exp[2], code)
        code.push(jump2)
        jump1.set_target(code.length)
        vm.compile(exp[3], code)
        jump2.set_target(code.length)
