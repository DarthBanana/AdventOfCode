## advent of code 2018
## https://adventofcode.com/2018
## day 21

import re
from computer import *

class Watch(Computer):
    def __init__(self):
        self.instmap = {}
        self.ip_bind = 0
        self.min_value = 1000000000000000000000000000
        self.values = set()
        self.count = 0
        Computer.__init__(self)
    def reset(self):                
        self.min_value = 1000000000000000000000000000
        self.values = set()
        self.count = 0
        Computer.reset(self)
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

    def pre_instruction(self):
        if self.ip == 28:
            print(self[3], self.min_value, self.count)
            if self[3] in self.values:
                return True
            self.values.add(self[3])
            self.min_value = min(self.min_value, self[3])
            self.count += 1

def fake_program(A):
    values = set()

    C = 0
    while True:
        B = C | 65536
        C = 10373714
        while True:
            C = C + (B & 255)
            C = C & 16777215
            C = C * 65899
            C = C & 16777215
            if 256 > B:
                break
            
            E = 0
            while True:
                D = E + 1
                D = D * 256
                if D > B:
                    break
                E = E + 1
            B = E
        print(C)
        if C in values:
            return
        values.add(C)
        print(C)
        if C == A:
            return
    



ip_re = re.compile(r"#ip (\d)")
class Puzzle:
    def __init__(self, lines):
        self.watch = Watch()

        first_line = lines.pop(0)
        self.watch.ip_bind = int(ip_re.search(first_line).group(1))
        self.watch.compile(lines)

    def part1(self):     
        self.watch[0] = 7967233   
        self.watch.run(False)
        return 7967233

    def part2(self):
        #fake_program(16477902)
        return 16477902