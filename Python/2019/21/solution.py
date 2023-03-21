## advent of code 2019
## https://adventofcode.com/2019
## day 21


from aocpuzzle import *
from computer import *
from intcode import *
    
PROGRAM_A = """\
NOT A T
NOT B J
OR T J
NOT C T
OR T J
AND D J
WALK
"""

# !(A & B & C) & D & (H | (E & I) | (E & F))
PROGRAM_F = """\
OR E J
AND F J
OR E T
AND I T
OR T J
OR H J
AND D J
NOT A T
NOT T T
AND B T
AND C T
NOT T T
AND T J
RUN
"""

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.computer = MyIntcodeComputer()
        self.computer.load_program_from_input(lines)

    def run_program(self, program):
        self.computer.reset()
        while(self.computer.can_continue()):
            self.computer.run()
            while(len(self.computer.tx_mailbox)):
                v = self.computer.tx_mailbox.receive()
                if v > 256:
                    print(v)
                    return v
                print(chr(v), end="")
            for c in program:
                self.computer.rx_mailbox.send(ord(c))

    def part1(self):
        return self.run_program(PROGRAM_A)

    def part2(self):
        print("PART 2")
        return self.run_program(PROGRAM_F)