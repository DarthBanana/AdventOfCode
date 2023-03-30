## advent of code 2020
## https://adventofcode.com/2020
## day 16

from aocpuzzle import *
from parsehelp import *

class TicketField:
    def __init__(self, line):
        self.name, ranges = line.split(': ')
        self.ranges = []
        for r in ranges.split(' or '):
            min, max = r.split('-')
            self.ranges.append((int(min), int(max)))
        self.index = -1

    def is_valid(self, value):        
        for r in self.ranges:
            if value >= r[0] and value <= r[1]:
                return True
        return False    
    
    def set_candidate_columns(self, n):
        self.candidates = set(range(n))
    
    def remove_candidate(self, n):
        if n in self.candidates:
            self.candidates.remove(n)


    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.always_run_part_1 = True
        self.fields = []
        stage = "fields"
        self.tickets = []
        for line in lines:            
            if stage == "fields":
                if line == '':
                    stage = "my ticket"
                    continue
        
                self.fields.append(TicketField(line))
            elif stage == "my ticket":
                if line == '':
                    stage = "nearby tickets"
                    continue

                if line.startswith('your ticket:'):
                    continue                
                self.my_ticket = get_all_ints(line)
            elif stage == "nearby tickets":
                if line.startswith('nearby tickets:'):
                    continue

                self.tickets.append(get_all_ints(line))        

    def resolve_fields(self):

        for f in self.fields:
            f.set_candidate_columns(len(self.my_ticket))                
            for i in range(len(self.tickets[0])):
                for t in self.tickets:
                    if not f.is_valid(t[i]):
                        f.remove_candidate(i)                        
                        break            
        resolved_columns = set()
        unresolved_fields = list(self.fields)

        while len(unresolved_fields) > 0:
            unresolved_fields.sort(key=lambda f: len(f.candidates))            
            f = unresolved_fields[0]            
            assert(len(f.candidates) == 1)

            index = f.candidates.pop()
            f.index = index
            resolved_columns.add(f.index)
            unresolved_fields.remove(f)

            for f in unresolved_fields:
                if index in f.candidates:
                    f.candidates.remove(index)
                                              

    def part1(self):
        bad_values = []
        bad_tickets = []
        for t in self.tickets:
            for v in t:
                valid = False
                for f in self.fields:
                    if f.is_valid(v):
                        valid = True
                        break
                if not valid:
                    bad_values.append(v)
                    if t not in bad_tickets:
                        bad_tickets.append(t)
        print(bad_values)
        for t in bad_tickets:
            self.tickets.remove(t)
        return sum(bad_values)
                    


    def part2(self):
        self.resolve_fields()
        result = 1
        count = 0
        for f in self.fields:
            if f.name.startswith('departure'):
                result *= self.my_ticket[f.index]
                count += 1
        assert(count == 6)
        return result