from ..scanner.token_scanner import TokenScanner
from ..parser.parser import Parser


class VM:
    def __init__(self):
        self.reset()
        self.globals = {}
        self.operators = {}
        self.functions = {}

    def run(self, code):
        self.reset()
        self.call("<stmt>", code)
        while self.cf is not None:
            self.step()
        return self.operand_stack.pop()

    def reset(self):
        self.operand_stack = []
        self.frame_stack = []
        self.cf = None

    def compile(self, exp, code, fn_name):
        if type(exp) is list:
            fn = exp[0]
            op = self.operators[fn]
            if not op:
                raise Exception('Undefined operator "{}"'.format(op))
            op.compile(self, exp, code, fn_name)
        else:
            token_type = TokenScanner.get_token_type(exp)
            if token_type == TokenScanner.WORD:
                code.append(LoadIns(exp))
            elif token_type == TokenScanner.NUMBER:
                code.append(PushIns(TokenScanner.get_number()))
            elif token_type == TokenScanner.STRING:
                code.append(PushIns(TokenScanner.get_string()))

    def define_operator(self, op):
        self.operators[op.name] = op

    def push(self, value):
        self.operand_stack.append(value)

    def pop(self):
        if len(self.operand_stack) == 0:
            raise Exception("Internal error: Operand stack empty")
        return self.operand_stack.pop()

    def top(self):
        if len(self.operand_stack) == 0:
            raise Exception("Internal error: Operand stack empty")
        return self.operand_stack[-1]

    def call(self, name, code):
        self.frame_stack.append(self.cf)
        self.cf = VMFrame(name, code)
        self.cf.scope_chain = VMScope()

    def ret(self):
        self.cf = self.frame_stack.pop()

    def step(self):
        if self.cf is None:
            return
        if self.cf.pc < len(self.cf.code):
            pc = self.cf.pc
            self.cf.code[pc].execute(self)
            if self.cf:
                self.cf.pc += 1
        else:
            self.ret()

    def get(self, id):
        scope = self.cf.scope_chain
        while scope is not None:
            value = scope.bindings[id]
            if value is not None:
                return value
            scope = scope.link
        return self.globals[id]

    def set(self, id, value):
        self.globals[id] = value

    def __str__(self):
        return str(type(self) + "(...)")


class PushIns:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "push " + Parser.unparse(self.value)

    def execute(self, vm):
        vm.push(self.value)


class PopIns:
    def __str__(self):
        return "push"

    def execute(self, vm):
        vm.pop()


class LoadIns:
    def __init__(self, variable):
        self.variable = variable

    def __str__(self):
        return "load " + self.variable

    def execute(self, vm):
        vm.push(vm.get(self.variable))


class StoreIns:
    def __init__(self, variable):
        self.variable = variable

    def __str__(self):
        return "store " + self.variable

    def execute(self, vm):
        vm.set(self.variable, vm.top())


class DupIns:
    def __str__(self):
        return "dup"

    def execute(self, vm):
        vm.push(vm.top())


class JumpIns:
    def __init__(self, name, target=None):
        self.name = name
        self.target = target

    def __str__(self):
        return self.name + " " + self.target

    def execute(self, vm):
        cond = True
        if self.name in ["jumpt", "jumpf"]:
            cond = not not vm.pop() is (self.name is "jumpt")
        if cond:
            vm.cf.pc = self.target

    def set_target(self, target):
        self.target = target


class CallIns:
    def __init__(self, fn=None):
        self.name = "call"
        self.fn = fn

    def __str__(self):
        return "call " + self.fn

    def compile(self, vm, exp, code):
        fn = exp[1]
        nargs = len(exp) - 2
        for i in range(0, nargs):
            vm.compile(exp[2 + i], code)
        code.push(PushIns(nargs))
        code.push(CallIns(fn))


class ReturnIns:
    def __init__(self):
        self.name = "return"

    def __str__(self):
        return self.name

    def compile(self, vm, exp, code):
        if len(exp) > 1:
            vm.compile(exp[1], code)
            code.push(self)

    def execute(self, vm):
        vm.ret()


class InfixOp:
    def __init__(self, name, fn):
        self.name = name
        self.fn = fn

    def __str__(self):
        return self.name

    def compile(self, vm, exp, code):
        vm.compile(exp[1], code)
        vm.compile(exp[2], code)
        code.push(self)

    def execute(self, vm):
        rhs = vm.pop()
        lhs = vm.pop()
        vm.push(self.fn(lhs, rhs))


class PrefixOp:
    def __init__(self, name, fn):
        self.name = "pre" + name
        self.fn = fn

    def __str__(self):
        return self.name

    def compile(self, vm, exp, code):
        vm.compile(exp[1], code)
        code.push(self)

    def execute(self, vm):
        vm.push(self.fn(vm.pop()))


class PostfixOp:
    def __init__(self, name, fn):
        self.name = "post" + name
        self.fn = fn

    def __str__(self):
        return self.name

    def compile(self, vm, exp, code):
        vm.compile(exp[1], code)
        code.push(self)

    def execute(self, vm):
        vm.push(self.fn(vm.pop()))


class AssignOp:
    def __init__(self, name, fn=None):
        self.name = name
        self.fn = fn

    def __str__(self):
        return self.name

    def compile(self, vm, exp, code):
        if self.fn:
            vm.compile(exp[1], code)
        vm.compile(exp[2], code)
        if self.fn:
            code.push(self)
        code.push(StoreIns(exp[1]))

    def execute(self, vm):
        rhs = vm.pop()
        lhs = vm.pop()
        vm.push(self.fn(lhs, rhs))


class VMFrame:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.pc = 0
        self.scope_chain = None


class VMScope:
    def __init__(self):
        self.bindings = {}
        self.link = None
