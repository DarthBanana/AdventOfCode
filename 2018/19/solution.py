## advent of code 2018
## https://adventofcode.com/2018
## day 19

import re
from computer import *

class Watch(Computer):
    def __init__(self):
        self.instmap = {}
        self.ip_bind = 0
        Computer.__init__(self)

    def advance_ip(self):
        self.ip = self[self.ip_bind]
        self.ip += 1
        self[self.ip_bind] = self.ip


    def addr(self, a, b, c):
        self[c] = self[a] + self[b]
        self.advance_ip()
    def addi(self, a, b, c):
        
        self[c] = self[a] + b
        self.advance_ip()
    def mulr(self, a, b, c):
        
        self[c] = self[a] * self[b]
        self.advance_ip()
    def muli(self, a, b, c):
        
        self[c] = self[a] * b
        self.advance_ip()
    def banr(self, a, b, c):
        self[c] = self[a] & self[b]
        self.advance_ip()
    def bani(self, a, b, c):
        self[c] = self[a] & b
        self.advance_ip()  
    def borr(self, a, b, c):
        self[c] = self[a] | self[b]
        self.advance_ip()
    def bori(self, a, b, c):
        self[c] = self[a] | b
        self.advance_ip()
    def setr(self, a, b, c):
        self[c] = self[a]
        self.advance_ip()     
    def seti(self, a, b, c):
        self[c] = a
        self.advance_ip()     
    def gtir(self, a, b, c):
        if a > self[b]:
            self[c] = 1
        else:
            self[c] = 0
        self.advance_ip()         
    def gtri(self, a, b, c):
        if self[a] > b:
            self[c] = 1
        else:
            self[c] = 0
        self.advance_ip()     
    def gtrr(self, a, b, c):
        if self[a] > self[b]:
            self[c] = 1
        else:
            self[c] = 0
        self.advance_ip()  
    def eqir(self, a, b, c):
        if a == self[b]:
            self[c] = 1
        else:
            self[c] = 0
        self.advance_ip()         
    def eqri(self, a, b, c):
        if self[a] == b:
            self[c] = 1
        else:
            self[c] = 0
        self.advance_ip()     
    def eqrr(self, a, b, c):
        if self[a] == self[b]:
            self[c] = 1
        else:
            self[c] = 0
        self.advance_ip()  

    def divb(self, a, b, c):
        if self[a] % self[b] == 0:
            self[c] = 1
        else:
            self[c] = 0
        self.advance_ip()

    def cdiv(self, a, b, c):
        for y in range(1, self[a]+1):
            if self[a] % y == 0:
                self[c] = self[c] + y
        self.advance_ip()

    def command_conversion(self, items):
        converted = []
        converted.append(items[0])
        for e in items[1:]:
            converted.append(int(e))
        return converted

ip_re = re.compile(r"#ip (\d)")
class Puzzle:
    def __init__(self, lines):
        self.watch = Watch()

        first_line = lines.pop(0)
        self.watch.ip_bind = int(ip_re.search(first_line).group(1))
        self.watch.compile(lines)

    def part1(self):        
        self.watch.run()
        return self.watch[0]

    def part2(self):
        self.watch.reset()
        self.watch[0] = 1
        self.watch.run()
        return self.watch[0]
        