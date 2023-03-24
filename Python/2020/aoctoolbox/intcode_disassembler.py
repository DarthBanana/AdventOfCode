OP_ADD = 1
OP_MUL = 2
OP_INPUT = 3
OP_OUTPUT = 4
OP_JIT = 5
OP_JIF = 6
OP_LT = 7
OP_EQ = 8
OP_SETREL = 9
OP_HALT = 99

INSTR_ARGS = {
    OP_ADD: 3,
    OP_MUL: 3,
    OP_INPUT: 1,
    OP_OUTPUT: 1,
    OP_JIT: 2,
    OP_JIF: 2,
    OP_LT: 3,
    OP_EQ: 3,
    OP_SETREL: 1,
    OP_HALT: 0,
}
INSTR_NM = {
    OP_ADD: 'add',
    OP_MUL: 'mul',
    OP_INPUT: 'input',
    OP_OUTPUT: 'output',
    OP_JIT: 'jit',
    OP_JIF: 'jif',
    OP_LT: 'lt',
    OP_EQ: 'eq',
    OP_SETREL: 'setrel',
    OP_HALT: 'halt',
}


def read_program(f):
    if not hasattr('read', f):
        # Hacky.  Not closed
        f = open(f, 'r')

    prog = []
    for line in f:
        for n in line.split(','):
            try:
                prog.append(int(n))
            except ValueError:
                pass # Just ignore newlines
    return prog


def might_be_instr(x):
    modes = str(x // 100)
    op = x % 100
    if op not in INSTR_NM:
        return False

    if len(modes) > INSTR_ARGS[op]:
        return False

    for d in modes:
        if d not in '012':
            return False

    return True


def fmt_instr(mem, idx):
    def fmt_arg(x, code):
        if code == 2:  # Relative
            return f'r[{x:+d}]'
        elif code == 1:  # Immediate
            return str(x)
        else:  # Position
            return f'[{x}]'
        return 'ARG'

    modes = mem[idx] // 100
    op = mem[idx] % 100

    argstr = ', '.join(fmt_arg(mem[idx + j + 1], (modes // 10**j) % 10)
                       for j in range(INSTR_ARGS[op]))
    return f'{INSTR_NM[op]} {argstr:24}\t{mem[idx:idx + 1 + INSTR_ARGS[op]]}'


def disassem(mem):
    i = 0
    while i < len(mem):
        if might_be_instr(mem[i]):
            modes = mem[i] // 100
            op = mem[i] % 100
            print(f'[{i:8}]    {fmt_instr(mem, i)}')
            i += 1 + INSTR_ARGS[op]
        else:
            print(f'[{i:8}]    DATA    {mem[i]}')
            i += 1

def interpret(mem):
    i = 0
    while i < len(mem):
        if might_be_instr(mem[i]):
            modes = mem[i] // 100
            op = mem[i] % 100
            print(f'[{i:8}]    {fmt_instr(mem, i)}')
            i += 1 + INSTR_ARGS[op]
        else:
            print(f'[{i:8}]    DATA    {mem[i]}')
            i += 1