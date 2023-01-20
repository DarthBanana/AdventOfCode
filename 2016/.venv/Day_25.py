import copy
import math
import os
import re
import time


PROGRAM = """\
cpy a d
cpy 11 c
cpy 231 b
inc d
dec b
jnz b -2
dec c
jnz c -5
cpy d a
jnz 0 0
cpy a b
cpy 0 a
cpy 2 c
jnz b 2
jnz 1 6
dec b
dec c
jnz c -4
inc a
jnz 1 -7
cpy 2 b
jnz c 2
jnz 1 4
dec b
dec c
jnz 1 -4
jnz 0 0
out b
jnz a -19
jnz 1 -21"""

OPTIMIZED = """\
cpy a d
cpy 11 c
cpy 231 b
inc d
dec b
jnz b -2
dec c
jnz c -5
cpy d a
jnz 0 0
cpy a b
cpy 0 a
cpy 2 c
dec_by c b
jnz 1 6
dec b
dec c
jnz c -4
inc a
jnz 1 -7
cpy 2 b
dec_by b c
jnz 1 4
dec b
dec c
jnz 1 -4
jnz 0 0
out b
jnz a -19
jnz 1 -21"""



REGISTER_VALUE = 2
REGISTER_ID = 4
REGISTER = 6
VALUE = 1


class Parameter:
    def __init__(self, param_type, value):
        self.type = param_type
        self.value = value

    def is_type(self, param_type):
        return self.type & param_type

    def __repr__(self):
        if self.type == VALUE:
            return "% s" % self.value
        else:
            return "Register(% s)" % self.value

    def is_equal(self, other):
        if self.type == other.type and self.value == other.value:
            return True
        return False


def are_params_valid(requirements, params):
    if len(requirements) != len(params):
        print("Invalid num params")
        return False

    for i in range(len(requirements)):
        if not params[i].is_type(requirements[i]):
            print("Invalid Parameter ", i)
            return False

    return True


def each_cons(x, size):
    for i in range(len(x)-size + 1):
        yield x[i:i+size], i


class Computer:

    def __init__(self):

        self.registers = [0, 0, 0, 0]
        self.ip = 0
        self.dirty = False
        self.output = []

    def print_instruction(self, instruction):
        func, params = instruction

        if func == self.cpy:
            print("cpy ", end="")
        elif func == self.inc:
            print("inc ", end="")
        elif func == self.dec:
            print("dec ", end="")
        elif func == self.jnz:
            print("jnz ", end="")
        elif func == self.tgl:
            print("tgl ", end="")
        elif func == self.inc_by:
            print("inc_by ", end="")
        elif func == self.inc_by_mult:
            print("inc_by_mult ", end="")
        elif func == self.dec_by:
            print("dec_by ", end="")
        elif func == self.out:
            print("out ", end="")
        else:
            print(func)
            assert (False)

        for param in params:
            if param.type == VALUE:
                print(param.value, " ", end="")
            else:
                if param.value == 0:
                    print("a ", end="")
                elif param.value == 1:
                    print("b ", end="")
                elif param.value == 2:
                    print("c ", end="")
                elif param.value == 3:
                    print("d ", end="")        
        print()

    def print_instructions(self, instructions):
        ip = 0
        for instruction in instructions:
            print(ip, ": ", end="")
            self.print_instruction(instruction)
            ip += 1

    def optimize(self):
        opt = copy.copy(self.instructions)
        inc_by_series = (self.inc, self.dec, self.jnz)
        inc_by_series2 = (self.dec, self.inc, self.jnz)
        dec_by_series = (self.dec, self.dec, self.jnz)        
        inc_by_mult_series = (self.cpy, self.inc_by,
                              self.dec, self.jnz, self.dec, self.jnz)
        # x += y
        # inc a
        # dec d
        # jnz d -2
        # -> inc_by a d

        for (a, b, c), i in each_cons(opt, 3):

            if (a[0], b[0], c[0]) == inc_by_series:
                if c[1][0].is_equal(b[1][0]):
                    if c[1][1].value == -2:
                        opt[i] = (self.inc_by, (a[1][0], b[1][0]))

            if (a[0], b[0], c[0]) == inc_by_series2:
                if c[1][0].is_equal(a[1][0]):
                    if c[1][1].value == -2:
                        opt[i] = (self.inc_by, (b[1][0], a[1][0]))


        # x += y * x
        # cpy b c
        # inc a -> inc_by a c
        # dec c
        # jnz c -2
        # dec d
        # jnz d -5
        # -> inc_by_mul a d b c
        for (a, b, c, d, e, f), i in each_cons(opt, 6):
            if not (a[0], b[0], c[0], d[0], e[0], f[0]) == inc_by_mult_series:
                continue
            if (not b[1][1].is_equal(a[1][1])):
                continue
            if (f[1][0].is_equal(e[1][0]) and (f[1][1].is_equal(Parameter(VALUE, -5)))):
                opt[i] = (self.inc_by_mult,
                          (b[1][0], a[1][0], a[1][1], e[1][0]))
        return opt

    def unpack_params(self, requirements, params):
        unpacked = []
        for i in range(len(requirements)):
            req = requirements[i]
            param = params[i]
            if param.type == REGISTER and req & REGISTER_VALUE:
                unpacked.append(self.registers[param.value])
            else:
                unpacked.append(param.value)
        if len(unpacked) == 1:
            return unpacked[0]
        return unpacked

    def inc_by(self, params):
        requirements = (REGISTER_ID, REGISTER_ID)
        if not are_params_valid(requirements, params):
            self.ip += 1
            return

        x, y = self.unpack_params(requirements, params)
        self.registers[x] += self.registers[y]
        self.registers[y] = 0
        self.ip += 3
    
    def dec_by(self, params):
        requirements = (REGISTER_ID, REGISTER_ID)
        if not are_params_valid(requirements, params):
            self.ip += 1
            return

        x, y = self.unpack_params(requirements, params)
        self.registers[x] -= self.registers[y]
        self.registers[y] = 0
        self.ip += 1

    def inc_by_mult(self, params):
        # a += b * d; d = 0; c = 0 (b might be reg or value)
        # inc_by_mult a b c d
        # w += x * y
        # z = 0
        # y = 0
        requirements = (REGISTER_ID, REGISTER_VALUE |
                        VALUE, REGISTER_ID, REGISTER_ID)

        if not are_params_valid(requirements, params):
            self.ip += 1
            return

        a, b, c, d = self.unpack_params(requirements, params)

        self.registers[a] += (b * self.registers[d])

        self.registers[c] = 0
        self.registers[d] = 0

        self.ip += 6

    def cpy(self, params):
        requirements = (REGISTER_VALUE | VALUE, REGISTER_ID)
        if not are_params_valid(requirements, params):
            self.ip += 1
            return

        x, y = self.unpack_params(requirements, params)

        self.registers[y] = x

        self.ip += 1

    def inc(self, params):
        requirements = (REGISTER_ID,)
        if not are_params_valid(requirements, params):
            self.ip += 1
            return

        x = self.unpack_params(requirements, params)

        self.registers[x] += 1
        self.ip += 1

    def dec(self, params):
        requirements = (REGISTER_ID,)
        if not are_params_valid(requirements, params):
            self.ip += 1
            return

        x = self.unpack_params(requirements, params)
        val = self.registers[x]
        self.registers[x] -= 1
        self.ip += 1

    def jnz(self, params):

        requirements = (REGISTER_VALUE | VALUE, REGISTER_VALUE | VALUE)
        if not are_params_valid(requirements, params):
            self.ip += 1
            return

        x, y = self.unpack_params(requirements, params)

        if not (x == 0):
            self.ip += y
        else:
            self.ip += 1

    def tgl(self, params):
        requirements = (REGISTER_VALUE | VALUE,)
        if not are_params_valid(requirements, params):
            self.ip += 1
            return

        x = self.unpack_params(requirements, params)

        target_ip = self.ip + x
        if not 0 <= target_ip < len(self.instructions):
            self.ip += 1
            return

        instruction, params = self.instructions[target_ip]
        if len(params) == 1:
            if instruction == self.inc:
                instruction = self.dec
            else:
                instruction = self.inc
            self.instructions[target_ip] = (instruction, params)
        else:
            if instruction == self.jnz:
                instruction = self.cpy
            else:
                instruction = self.jnz

            self.instructions[target_ip] = (instruction, params)

        self.ip += 1
        return True

    def out(self, params):
        requirements = (REGISTER_VALUE | VALUE,)
        if not are_params_valid(requirements, params):
            self.ip += 1
            return

        x = self.unpack_params(requirements, params)

        self.output.append(x)
        self.ip += 1

    def compile_instruction(self, instruction_string):
        registers = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
        cpy_reg_re = re.compile(r"cpy (\w) (\w)")
        cpy_int_re = re.compile(r"cpy (-*\d+) (\w)")
        inc_re = re.compile(r"inc (\w)")
        dec_re = re.compile(r"dec (\w)")
        jnz_re = re.compile(r"jnz (\w) (-*\d+)")
        jnz_int_re = re.compile(r"jnz (\d+) (-*\d+)")
        jnz_int_reg_re = re.compile(r"jnz (\d+) (\w)")
        tgl_re = re.compile(r"tgl (\w)")
        out_re = re.compile(r"out (\w)")
        out_int_re = re.compile(r"out (-*\d+)")
        dec_by_re = re.compile(r"dec_by (\w) (\w)")
        # print(instruction_string)

        match = cpy_int_re.search(instruction_string)
        if (match):
            return (self.cpy, (Parameter(VALUE, int(match.group(1))), Parameter(REGISTER, registers[match.group(2)])))

        match = cpy_reg_re.search(instruction_string)
        if (match):
            return (self.cpy, (Parameter(REGISTER, registers[match.group(1)]), Parameter(REGISTER, registers[match.group(2)])))

        match = inc_re.search(instruction_string)
        if (match):
            return (self.inc, (Parameter(REGISTER, registers[match.group(1)]),))

        match = dec_re.search(instruction_string)
        if (match):
            return (self.dec, (Parameter(REGISTER, registers[match.group(1)]),))

        match = jnz_int_re.search(instruction_string)
        if (match):
            return (self.jnz, (Parameter(VALUE, int(match.group(1))), Parameter(VALUE, int(match.group(2)))))

        match = jnz_re.search(instruction_string)
        if (match):
            return (self.jnz, (Parameter(REGISTER, registers[match.group(1)]), Parameter(VALUE, int(match.group(2)))))

        match = jnz_int_reg_re.search(instruction_string)
        if (match):

            return (self.jnz, (Parameter(VALUE, int(match.group(1))), Parameter(REGISTER, registers[match.group(2)])))

        match = tgl_re.search(instruction_string)
        if (match):
            return (self.tgl, (Parameter(REGISTER, registers[match.group(1)]),))

        match = out_re.search(instruction_string)
        if (match):
            return (self.out, (Parameter(REGISTER, registers[match.group(1)]),))
        
        match = out_int_re.search(instruction_string)
        if (match):
            return (self.out, (Parameter(VALUE, int(match.group(1))),))

        match = dec_by_re.search(instruction_string)
        if (match):
            return (self.dec_by, (Parameter(REGISTER, registers[match.group(1)]), Parameter(REGISTER, registers[match.group(2)])))
            
        assert (False)

    def compile_instructions(self, program):
        instructions = []
        for line in program.splitlines():
            instructions.append(self.compile_instruction(line))

        self.instructions = instructions

    def execute_instruction(self, instruction):

        #self.print(self.ip, ": ", end="")
        #self.print_instruction(instruction)
        func, params = instruction
        result = func(params)
        #print(self.registers)
        #time.sleep(.2)
        return result

    def execute_program(self,length):
                
        instructions = self.instructions
        opt = self.optimize()

        while 0 <= self.ip < len(instructions) and len(self.output) < length:
            #print(self.ip, ": ", end="")
            if self.execute_instruction(opt[self.ip]):
                opt = self.optimize()            

    def reset(self, a):
        self.output = []
        self.registers = [a, 0, 0, 0]
        self.ip = 0


computer = Computer()
computer.compile_instructions(OPTIMIZED)

# I give up, just hand decoding this:
def simulate_program(a, length):
    output = []
    d = a + 2541
    while(True):
        a = d
        while not a == 0:
            b = a % 2
            a = a//2
            output.append(b)
            if len(output) == length:
                return output

def test_them():

    a = 0
    while (True):    
        last = 0
        result = simulate_program(a, 100)
        last = result[0]
        found = True
        for out in result[1:]:
            if not (out ==  last ^ 1):
                found = False
                break
            last = out
        if found:
            print(result)
            return a
        a += 1



# Greater than 158
print(test_them())
#x = 0
#while(True):
#    computer.reset(x)
#    computer.execute_program(16)
#    print(x,computer.output)
#    if computer.output[0] != computer.output[1]:
#        break
#    x += 1
#    if x > 100:
#        break;

    

