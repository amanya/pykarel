from ..vm.vm import JumpIns, PushIns, StoreIns, LoadIns
from ..vm.xvm import XVM


class KarelVM(XVM):
    def __init__(self, karel):
        XVM.__init__(self)
        self.karel = karel
        self.init_karel_operators()
        self.user_fn_names = []
        self.next_temp = 0

    def init_karel_operators(self):
        self.define_operator(KarelCall())
        self.define_operator(KarelWhile())
        self.define_operator(KarelRepeat())
        self.define_operator(KarelIf())
        self.define_operator(KarelBlock())
        self.define_operator(KarelStmt())

    def reset_temp_counter(self):
        self.next_temp = 0

    def set_user_fn_names(self, user_fn_names):
        self.user_fn_names = user_fn_names

    def start_check(self):
        if self.cf is None:
            code = self.functions["main"]
            if not code:
                raise Exception("No main function defined")
            self.call("main", code)

    def at_statement_boundary(self):
        return not self.cf or self.cf.code[self.cf.pc].name == "stmt"


class KarelCall:
    def __init__(self, fn=None):
        self.name = "call"
        self.fn = fn

    def __str__(self):
        return self.name + " " + self.fn

    def legal_fn(self, fn, vm):
        if fn in vm.karel.instructions:
            return True
        if fn in vm.karel.predicates:
            return True
        if fn in vm.user_fn_names:
            return True
        return False

    def compile(self, vm, exp, code, fn_name):
        fn = exp[1]
        if not self.legal_fn(fn, vm):
            raise Exception('Undefined operator "{}"'.format(fn))
        code.append(KarelCall(fn))

    def execute(self, vm):
        if self.fn in vm.karel.instructions:
            getattr(vm.karel, self.fn)()
        elif self.fn in vm.karel.predicates:
            predicate = getattr(vm.karel, self.fn)
            vm.push(predicate())
        else:
            vm.call(self.fn, vm.functions[self.fn])


class KarelRepeat:
    def __init__(self):
        self.name = "repeat"

    def __str__(self):
        return self.name

    def compile(self, vm, exp, code, fn_name):
        temp = "$" + fn_name + str(vm.next_temp)
        vm.next_temp += 1
        jump1 = JumpIns("jumpf")
        jump2 = JumpIns("jump")
        code.append(PushIns(exp[1]))
        code.append(StoreIns(temp))
        jump2.set_target(len(code))
        code.append(PushIns(0))
        code.append(vm.operators[">"])
        code.append(jump1)
        vm.compile(exp[2], code)
        code.append(LoadIns(temp))
        code.append(PushIns(1))
        code.append(vm.operators["-"])
        code.append(StoreIns(temp))
        code.append(jump2)
        jump1.set_target(len(code))


class KarelWhile:
    def __init__(self):
        self.name = "while"

    def __str__(self):
        return self.name

    def compile(self, vm, exp, code, fn_name):
        jump1 = JumpIns("jumpf")
        jump2 = JumpIns("jump")
        jump2.set_target(len(code))
        vm.compile(exp[1], code)
        code.append(jump1)
        vm.compile(exp[2], code)
        code.append(jump2)
        jump1.set_target(len(code))


class KarelIf:
    def __init__(self):
        self.name = "if"

    def __str__(self):
        return self.name

    def compile(self, vm, exp, code, fn_name):
        jump1 = JumpIns("jumpf")
        jump2 = JumpIns("jump")
        vm.compile(exp[1], code)
        code.append(jump1)
        vm.compile(exp[2], code)
        if len(exp) > 3:
            code.append(jump2)
            jump1.set_target(len(code))
            vm.compile(exp[3], code)
            jump2.set_target(len(code))
        else:
            jump1.set_target(len(code))


class KarelBlock:
    def __init__(self):
        self.name = "block"

    def __str__(self):
        return self.name

    def compile(self, vm, exp, code, fn_name):
        for i in range(1, len(exp)):
            vm.compile(exp[i], code, fn_name)


class KarelStmt:
    def __init__(self):
        self.name = "stmt"

    def __str__(self):
        return self.name

    def compile(self, vm, exp, code, fn_name):
        code.append(self)
        vm.compile(exp[1], code, fn_name)

    def execute(self, vm):
        pass
