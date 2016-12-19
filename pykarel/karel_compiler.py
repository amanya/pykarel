from .karel.karel_parser import KarelParser
from .karel.karel_vm import KarelVM
from .vm.vm import ReturnIns


class KarelCompiler:
    def __init__(self, karel):
        self.vm = KarelVM(karel)

    def compile(self, text):
        parser = KarelParser()
        parser.set_input(text)
        functions = []
        function_names = []
        while True:
            token = parser.next_token()
            if token is "":
                break
            parser.save_token(token)
            fn = parser.read_function()
            functions.append(fn)
            function_names.append(fn[1])
        self.vm.set_user_fn_names(function_names)
        for i in range(0, len(functions)):
            fn = functions[i]
            code = []
            self.vm.reset_temp_counter()
            self.vm.compile(fn[2], code, function_names[i])
            code.append(ReturnIns())
            self.vm.functions[fn[1]] = code
        self.vm.reset()
        self.vm.start_check()

    def execute_step(self):
        vm = self.vm
        if not vm.cf:
            return True
        running = True
        while running:
            if vm.at_statement_boundary():
                running = False
            vm.step()
        return False

