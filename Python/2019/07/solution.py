## advent of code 2019
## https://adventofcode.com/2019
## day 07

from aocpuzzle import *
from aocpuzzle import *
from intcode import *
from parsehelp import *
from itertools import permutations

    

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test=False)
        self.input_mailbox = Mailbox()
        self.output_mailbox = Mailbox()
        
        self.ABmailbox = Mailbox()
        self.BCmailbox = Mailbox()
        self.CDmailbox = Mailbox()
        self.DEmailbox = Mailbox()
        self.AmpA = MyIntcodeComputer(self.input_mailbox, self.ABmailbox)
        self.AmpB = MyIntcodeComputer(self.ABmailbox, self.BCmailbox)
        self.AmpC = MyIntcodeComputer(self.BCmailbox, self.CDmailbox)
        self.AmpD = MyIntcodeComputer(self.CDmailbox, self.DEmailbox)
        self.AmpE = MyIntcodeComputer(self.DEmailbox, self.output_mailbox)

        self.code = get_all_ints(lines[0])
        self.AmpA.load_program(self.code)
        self.AmpB.load_program(self.code)
        self.AmpC.load_program(self.code)
        self.AmpD.load_program(self.code)
        self.AmpE.load_program(self.code)
        
        self.reset_all()

    def reset_all(self):
        self.AmpA.reset()
        self.AmpB.reset()
        self.AmpC.reset()
        self.AmpD.reset()
        self.AmpE.reset()
        self.amps = deque([self.AmpA, self.AmpB, self.AmpC, self.AmpD, self.AmpE])
    def setup_phase(self, phase):
        self.input_mailbox.send(phase[0])
        self.ABmailbox.send(phase[1])
        self.BCmailbox.send(phase[2])
        self.CDmailbox.send(phase[3])
        self.DEmailbox.send(phase[4])
        self.input_mailbox.send(0)

    def part1(self):
        max_signal = 0
        for phase in permutations(range(5)):
            self.reset_all()
            self.setup_phase(phase)
            for amp in self.amps:
                amp.run()
            signal = self.output_mailbox.receive()
            if signal > max_signal:
                max_signal = signal
        return max_signal

    def part2(self):
        max_signal = 0
        self.output_mailbox.chain_output(self.input_mailbox)
        for phase in permutations(range(5, 10)):
            self.reset_all()
            self.setup_phase(phase)            
            while len(self.amps) > 0:
                amp = self.amps.popleft()
                amp.run()
                if amp.can_continue():
                    self.amps.append(amp)
            
            signal = self.input_mailbox.receive()
            if signal > max_signal:
                max_signal = signal
        return max_signal