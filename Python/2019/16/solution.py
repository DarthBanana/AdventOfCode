## advent of code 2019
## https://adventofcode.com/2019
## day 16

from aocpuzzle import *
def pattern_generator(n):
    while True:
        for i in range(n):
            yield 0
        for i in range(n):
            yield 1
        for i in range(n):
            yield 0
        for i in range(n):
            yield -1
            
class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.initial_signal = [int(c) for c in lines[0]]

    def calc_digit(self, signal, n):
        pattern = pattern_generator(n+1)
        next(pattern)
        new_value = 0
        for s in signal:
            p = next(pattern)            
            new_value += s * p
        result = abs(new_value) % 10        
        return result
    
    def execute_phase(self, signal):
        new_signal = []
        for i in range(len(signal)):
            new_signal.append(self.calc_digit(signal, i))
        return new_signal
    
    def part1(self):
        signal = self.initial_signal

        iterations = 100

        for phase in range(iterations):
            signal = self.execute_phase(signal)
            
        return ''.join([str(s) for s in signal[:8]])

    def part2(self):
        signal = self.initial_signal*10000
        iterations = 100
        offset = int(''.join([str(s) for s in signal[:7]]))
        signal = signal[offset:]
        for i in range(iterations):
            for j in range(len(signal)-2, -1, -1):
                signal[j] = (signal[j+1] + signal[j]) % 10
        return ''.join([str(s) for s in signal[:8]])
    