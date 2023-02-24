## advent of code 2018
## https://adventofcode.com/2018
## day 16
import re
from computer import *
before_re = re.compile(r"Before: \[(.*)\]")
after_re = re.compile(r"After:  \[(.*)\]")
code_re = re.compile(r"(\d*) (.*)")
class Rule():
    def __init__(self, before, after, code):
        #print(before)
        #print(code)
        #print(after)
        self.before = []
        self.after = []
        self.line = []
        self.inst = 0
        self.params = []
        match = before_re.search(before)
        num_strings = match.group(1).split(", ")
        for numstr in num_strings:
            self.before.append(int(numstr))
    
        match = after_re.search(after)
        num_strings = match.group(1).split(", ")
        for numstr in num_strings:
            self.after.append(int(numstr))
            
        
        for s in code.split():
            self.line.append(int(s))    
        self.inst = self.line[0]
        self.params = self.line[1:]

INSTRUCTIONS = ["addr", "addi", "mulr", "muli", "banr", "bani", "borr", "bori", "setr", "seti", "gtir", "gtri", "gtrr", "eqir", "eqri", "eqrr"]

class Watch(Computer):
    def __init__(self):
        self.instmap = {}
        Computer.__init__(self)

    def addr(self, a, b, c):
        self[c] = self[a] + self[b]
        self.ip += 1
    def addi(self, a, b, c):
        
        self[c] = self[a] + b
        self.ip += 1
    def mulr(self, a, b, c):
        
        self[c] = self[a] * self[b]
        self.ip += 1
    def muli(self, a, b, c):
        
        self[c] = self[a] * b
        self.ip += 1    
    def banr(self, a, b, c):
        self[c] = self[a] & self[b]
        self.ip += 1
    def bani(self, a, b, c):
        self[c] = self[a] & b
        self.ip += 1       
    def borr(self, a, b, c):
        self[c] = self[a] | self[b]
        self.ip += 1
    def bori(self, a, b, c):
        self[c] = self[a] | b
        self.ip += 1     
    def setr(self, a, b, c):
        self[c] = self[a]
        self.ip += 1          
    def seti(self, a, b, c):
        self[c] = a
        self.ip += 1          
    def gtir(self, a, b, c):
        if a > self[b]:
            self[c] = 1
        else:
            self[c] = 0
        self.ip += 1              
    def gtri(self, a, b, c):
        if self[a] > b:
            self[c] = 1
        else:
            self[c] = 0
        self.ip += 1          
    def gtrr(self, a, b, c):
        if self[a] > self[b]:
            self[c] = 1
        else:
            self[c] = 0
        self.ip += 1       
    def eqir(self, a, b, c):
        if a == self[b]:
            self[c] = 1
        else:
            self[c] = 0
        self.ip += 1              
    def eqri(self, a, b, c):
        if self[a] == b:
            self[c] = 1
        else:
            self[c] = 0
        self.ip += 1          
    def eqrr(self, a, b, c):
        if self[a] == self[b]:
            self[c] = 1
        else:
            self[c] = 0
        self.ip += 1       

    def func_name_conversion(self, command):
        return self.instmap[command]
    def command_conversion(self, items):
        converted = []
        for e in items:
            converted.append(int(e))
        return converted
class Puzzle:
    def __init__(self, lines):
        self.watch = Watch()
        self.rules = []
        self.map = {}
        while(True):
            line = lines.pop(0)
            if before_re.search(line):
                code = lines.pop(0)
                after = lines.pop(0)
                self.rules.append(Rule(line, after, code))
                blank = lines.pop(0)
            else:
                break
        self.rest = lines
        self.rules.sort(key=lambda x: x.inst)

    def is_match(self, inst, rule):
        
        self.watch.reset()

        # set up initial conditions
        for i in range(len(rule.before)):
            self.watch.set_register(i, rule.before[i])
        
        # call function
        func = getattr(self.watch, inst)
        func(*rule.params)

        #check post condition
        for i in range(len(rule.after)):
            if not (self.watch[i] == rule.after[i]):
                return False
        return True

    def count_3_or_more_rules(self):
        global_count = 0
        for rule in self.rules:
            local_count = 0
            for inst in INSTRUCTIONS:
                if self.is_match(inst, rule):
                    local_count += 1
            if local_count > 2:
                global_count += 1

        return global_count

    def discover_instructions(self):
        possible_insts = []
        for i in range(16):
            possible_insts.append((i,INSTRUCTIONS.copy()))

        for rule in self.rules:
            id, insts = possible_insts[rule.inst]
            new_insts = []
            for inst in insts:
                if self.is_match(inst, rule):
                    new_insts.append(inst)
            possible_insts[rule.inst] = (id, new_insts)


        while(possible_insts):
            possible_insts.sort(key=lambda x:len(x[1]))
            id, insts = possible_insts.pop(0)

            if (len(insts) == 0):
                continue
            assert(len(insts) == 1)
            inst = insts[0]
            self.watch.instmap[id] = inst
            
            for id, insts in possible_insts:
                if inst in insts:
                    insts.remove(inst)



    def part1(self):
        
        return self.count_3_or_more_rules()

    def part2(self):
        self.discover_instructions()
        self.watch.reset()
        self.watch.compile(self.rest)
        self.watch.run()
        return self.watch[0]

        