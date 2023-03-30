## advent of code 2020
## https://adventofcode.com/2020
## day 18

from collections import deque
from aocpuzzle import *

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.reset()

    def reset(self):
        self.cracked_lines = [self.crack_line(line) for line in self.lines]

    def crack_line(self, line):        
        line = line.replace('(', '( ')
        line = line.replace(')', ' )')
        return deque(line.split(' '))
    
    def operate(self, operation, value, element):
        if operation == '+':
            value += int(element)
        elif operation == '*':
            value *= int(element)
        else:
            value = int(element)
        return value
    
    def solve_line(self, line):
        operation = None
        value = None
        while(len(line)):
            element = line.popleft()            
            if element == '(':                
                value = self.operate(operation, value, self.solve_line(line))                                
                operation = None
            elif element == ')':                
                return value
            elif element == '+':
                operation = '+'
            elif element == '*':
                operation = '*'
            else:
                value = self.operate(operation, value, element)                
                operation = None
        return value
    
    def solve_line2(self, line):
        # First solve all brackets
        new_line = deque()
        while(line.count('(') > 0 or line.count(')') > 0):
            while(len(line)):
                element = line.popleft()
                if element == '(':
                    new_line.append(self.solve_line2(line))
                elif element == ')':
                    break
                else:
                    new_line.append(element)
            line = new_line

        # Then solve all additions
        while(line.count('+') > 0):
            new_line = deque()
            while(len(line)):
                element = line.popleft()
                if element == '+':
                    new_line.append(int(new_line.pop()) + int(line.popleft()))
                else:
                    new_line.append(element)
            line = new_line

        # Then solve all multiplications
        value = 1
        while(len(line)):
            element = line.popleft()
            if element != '*':
                value *= int(element)
        return value

                    
    def part1(self):
        sum = 0
        for l in self.cracked_lines:
            sum += self.solve_line(l)
        return sum

    def part2(self):
        self.reset()
        sum = 0
        for l in self.cracked_lines:
            sum += self.solve_line2(l)
        return sum