from computer import *
from collections import deque

from parsehelp import get_all_ints

VARIABLE_NAMES = {}
NAME_CANDIDATES = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
VARIABLE_NAME_INDEX = 0
MAP_VARIABLE_NAMES = False


def new_variable():
    global VARIABLE_NAME_INDEX
    repeats = VARIABLE_NAME_INDEX // len(NAME_CANDIDATES)
    offset = VARIABLE_NAME_INDEX % len(NAME_CANDIDATES)
    name = NAME_CANDIDATES[offset] * (repeats + 1)
    VARIABLE_NAME_INDEX += 1
    return name


def get_var_name(raw):
    if MAP_VARIABLE_NAMES:

        if raw in VARIABLE_NAMES:
            return VARIABLE_NAMES[raw]
        else:
            name = new_variable()
            VARIABLE_NAMES[raw] = name
            return name
    else:
        return raw


class IntCodeParameter(Parameter):

    def __new__(self, mode, raw_value, address, value, destination=False):
        self.mode = mode
        return Parameter.__new__(self, raw_value, address, value, destination)

    def __init__(self, mode, raw_value, address, value, destination=False):
        self.mode = mode

        return Parameter.__init__(self, raw_value, address, value, destination)

    def __str__(self):
        if self.mode == 0:
            return "I{0}({1})".format(self.raw, int(self))
        elif self.mode == 1:
            return "D{0}".format(self.raw)
        elif self.mode == 2:
            return "R{0}({1})".format(self.raw, int(self))

    def interpret(self):
        if self.mode == 0:
            output = "M{0}".format(self.raw)
            return get_var_name(output)
        elif self.mode == 1:
            if self.destination:
                output = "M{0}".format(self.raw)
                return get_var_name(output)
            return str(int(self))
        elif self.mode == 2:
            if self.destination:
                return "M(base + {0})".format(self.raw)
            return "(base + {0})".format(self.raw)


class IntCodeParamListIter:
    def __init__(self, param_list):
        self.param_list = param_list
        self.index = 0

    def __iter__(self):
        return IntCodeParamListIter(self.param_list)

    def __next__(self):
        if self.index >= len(self.param_list):
            raise StopIteration
        result = self.param_list[self.index]
        self.index += 1
        return result


class IntCodeParamList:
    def __init__(self, instruction):
        self.instruction = instruction
        self.index = 0

    def __getitem__(self, k):
        return self.instruction.get_parameter(k)

    def __len__(self):
        return self.instruction.param_count

    def __iter__(self):
        return IntCodeParamListIter(self)


class IntCodeInstruction(Instruction):
    def __init__(self, ip, computer):
        self.raw_instruction = computer[ip]

        opcode = self.raw_instruction % 100

        if opcode not in computer.instruction_set:
            return None
        self.inst_descriptor = computer.instruction_set[opcode]
        func = self.inst_descriptor.func
        name = self.inst_descriptor.name
        self.param_count = self.inst_descriptor.param_count
        self.output_param_index = self.inst_descriptor.output_param_number - 1
        params = IntCodeParamList(self)
        self.computer = computer
        return Instruction.__init__(self, name, func, params, opcode, ip)

    def get_parameter(self, k):
        if k >= self.param_count:
            return None
        if k == self.output_param_index:
            return self.get_output_parameter(k+1)
        return self.get_input_parameter(k+1)

    def get_input_parameter(self, id):

        value = self.computer[self.ip + id]
        mode = self.raw_instruction % 10**(id+2) // 10**(id+1)

        if mode == 0:
            return self.computer[value]
        elif mode == 1:
            return value
        elif mode == 2:
            return self.computer[value + self.computer.relative_base]

    def get_output_parameter(self, id):

        mode = self.raw_instruction % 10**(id+2) // 10**(id+1)
        value = self.computer[self.ip + id]
        if mode == 0:
            return value
        elif mode == 1:
            return value
        elif mode == 2:
            return value + self.computer.relative_base
        else:
            assert (False)

    def execute(self):
        self.func(self.params)

    def interpret_param(self, k):
        if k >= self.param_count:
            return None
        output_param = False
        if k == self.output_param_index:
            output_param = True
        value = self.computer[self.ip + k + 1]
        mode = self.raw_instruction % 10**(k+2) // 10**(k+1)
        if mode == 0:
            output = "M{0}".format(value)
            return get_var_name(output)
        elif mode == 1:
            if output_param:
                output = "M{0}".format(value)
                return get_var_name(output)
            return str(value)
        elif mode == 2:
            if output_param:
                return "M(base + {0})".format(value)
            return "(base + {0})".format(value)

    def interpret(self):
        format_string = self.inst_descriptor.format_string
        param_values = []
        for i in range(self.param_count):
            param_values.append(self.interpret_param(i))

        return format_string.format(*param_values)


class IntcodeInstructionDescriptor(InstructionDescriptor):
    def __init__(self, name, func, param_count, output_param_number, format_string):
        self.param_count = param_count
        self.output_param_number = output_param_number

        return InstructionDescriptor.__init__(self, name, func, format_string)


class Mailbox:
    def __init__(self, verbose=False):
        self.mailbox = deque()
        self.verbose = verbose
        self.chained_output = None
        self.receive_routine = None

    def set_receive_routine(self, routine):
        self.receive_routine = routine

    def send(self, value: int):
        value = int(value)
        if self.verbose:
            print("SEND", value)
        if self.chained_output is not None:
            self.chained_output.send(value)
        elif self.receive_routine:
            self.receive_routine(self, value)
        else:
            self.mailbox.append(value)

    def chain_output(self, mailbox):
        self.chained_output = mailbox

    def receive(self):
        if len(self.mailbox) == 0:
            return None
        result = self.mailbox.popleft()
        if self.verbose:
            print("RECV", result)
        return result

    def __len__(self):
        return len(self.mailbox)

    def __str__(self):
        return str(list(self.mailbox))

    def reset(self):
        self.mailbox = deque()


class IntcodeComputer(ComputerRoot):
    def __init__(self):
        super().__init__()
        self.instruction_set = {}

    def reset(self):
        super().reset()
        self.relative_base = 0
        self.program = self.original_program.copy()
        self.memory = {}
        for i in range(len(self.original_program)):
            self.memory[i] = self.original_program[i]

    def load_program_from_input(self, lines):
        code = get_all_ints(lines[0])
        self.load_program(code)

    def set_instruction_set(self, instruction_set):
        self.instruction_set = instruction_set

    def __getitem__(self, k):
        if isinstance(k, Parameter):
            return self.memory.get(k.address, 0)
        else:
            return self.memory.get(k, 0)

    def __setitem__(self, k, value):
        if isinstance(k, Parameter):
            self.memory[k.address] = value
        else:
            self.memory[k] = value

    def is_ip_valid(self, ip):
        if ip < 0:
            return False
        if ip not in self.memory:
            return False
        return True

    def interpret_instruction(self, instruction):
        return instruction.interpret()

    def get_instruction(self, ip, for_interpretation=False):
        return IntCodeInstruction(ip, self)

    def advance_to_next_instruction(self, ip, instruction):
        inst_descriptor = self.instruction_set[instruction.opcode]

        return ip + inst_descriptor.param_count + 1


class MyIntcodeComputer(IntcodeComputer):
    def __init__(self, rx_mailbox = None, tx_mailbox = None):
        if tx_mailbox:
            self.tx_mailbox = tx_mailbox
        else:
            self.tx_mailbox = Mailbox()
        if rx_mailbox:            
            self.rx_mailbox = rx_mailbox
        else:
            self.rx_mailbox = Mailbox()
            
        IntcodeComputer.__init__(self)
        self.instmap = {
            1: IntcodeInstructionDescriptor("add", self.add, 3, 3, "{2} = {0} + {1}"),
            2: IntcodeInstructionDescriptor("mul", self.mul, 3, 3, "{2} = {0} * {1}"),
            3: IntcodeInstructionDescriptor("rcv", self.rcv, 1, 1, "{0} = rx"),
            4: IntcodeInstructionDescriptor("tx", self.tx, 1, 0, "tx({0})"),
            5: IntcodeInstructionDescriptor("jit", self.jit, 2, 0, "if {0} != 0: GOTO {1}"),
            6: IntcodeInstructionDescriptor("jif", self.jif, 2, 0, "if {0} == 0: GOTO {1}"),
            7: IntcodeInstructionDescriptor("lt", self.lt, 3, 3, "{2} = 1 if {0} < {1} else 0"),
            8: IntcodeInstructionDescriptor("eq", self.eq, 3, 3, "{2} = 1 if {0} == {1} else 0"),
            9: IntcodeInstructionDescriptor("srb", self.srb, 1, 0, "base += {0}"),
            99: IntcodeInstructionDescriptor("halt", self.halt, 0, 0, "halt")}
        self.set_instruction_set(self.instmap)

    def reset(self):
        IntcodeComputer.reset(self)
        self.rx_mailbox.reset()
        self.tx_mailbox.reset()

    def add(self, params):
        x = params[0]
        y = params[1]
        z = params[2]
        self[z] = x + y
        self.ip += 4

    def mul(self, params):
        x = params[0]
        y = params[1]
        z = params[2]
        self[z] = x * y
        self.ip += 4

    def jit(self, params):
        x = params[0]
        y = params[1]

        if x != 0:
            self.ip = y
        else:
            self.ip += 3

    def jif(self, params):
        x = params[0]
        y = params[1]
        if x == 0:
            self.ip = y
        else:
            self.ip += 3

    def lt(self, params):
        x = params[0]
        y = params[1]
        z = params[2]
        if x < y:
            self[z] = 1
        else:
            self[z] = 0
        self.ip += 4

    def eq(self, params):
        x = params[0]
        y = params[1]
        z = params[2]
        if x == y:
            self[z] = 1
        else:
            self[z] = 0
        self.ip += 4

    def srb(self, params):
        x = params[0]

        self.relative_base += x
        if self.verbose:
            print("relative base", self.relative_base)
        self.ip += 2

    def halt(self, params):
        self.ip = -1

    def rcv(self, params):
        x = params[0]
        if len(self.rx_mailbox) == 0:
            self.enter_wait_state()
            if self.verbose:
                print("waiting for input")
            return
        self[x] = self.rx_mailbox.receive()
        self.ip += 2

    def tx(self, params):
        x = params[0]
        self.tx_mailbox.send(x)
        self.ip += 2
