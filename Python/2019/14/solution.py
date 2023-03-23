## advent of code 2019
## https://adventofcode.com/2019
## day 14

from aocpuzzle import *
class Reaction(object):
    def __init__(self, line):
        self.inputs = []
        self.line = line
        inputs, output = line.split(' => ')
        
        inputs = inputs.split(', ')
        for input in inputs:
            input = input.split(' ')
            self.inputs.append((int(input[0]), input[1]))
        output = output.split(' ')
        
        self.output = (int(output[0]), output[1])
        self.normalized_inputs = [(input[0] / self.output[0], input[1]) for input in self.inputs]

    def __str__(self):
        return self.line
    def __repr__(self):
        return self.line

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)        
        self.reactions = {}
        for line in lines:
            reaction = Reaction(line)
            self.reactions[reaction.output[1]] = reaction
        print(self.reactions)
        self.spares = {}
        self.needs = {}
    
    def get_chemical_needs_fp(self, chemical, need):
        if chemical == 'ORE':
            return need
        
        reaction = self.reactions[chemical]        
        
        for input in reaction.normalized_inputs:            
            self.needs[input[1]] = self.needs.get(input[1], 0) + input[0] * need
            self.get_chemical_needs_fp(input[1], input[0] *need)
        
        return 


    def get_ore_count(self, chemical, needed):
        
        if chemical in self.spares:
            if self.spares[chemical] >= needed:
                self.spares[chemical] -= needed
                return 0
            else:
                needed -= self.spares[chemical]
                self.spares[chemical] = 0

        if chemical == 'ORE':
            return needed
        reaction = self.reactions[chemical]
        reactions_needed = needed // reaction.output[0] + (1 if needed % reaction.output[0] else 0)

        ore_count = 0
        for input in reaction.inputs:
            ore_count += self.get_ore_count(input[1], input[0] * reactions_needed)

        if reactions_needed * reaction.output[0] > needed:
            self.spares[chemical] = reactions_needed * reaction.output[0] - needed        
        return ore_count
    
    def part1(self):

        return self.get_ore_count('FUEL', 1)

    def part2(self):
        self.get_chemical_needs_fp('FUEL', 1)
        needs = self.needs["ORE"]
        ore = 1000000000000
        output = ore / needs
        print(output)
        intoutput = int(output)
        print(intoutput)
        print(self.get_ore_count('FUEL', intoutput+1))
        print(self.get_ore_count('FUEL', intoutput))
        print(self.get_ore_count('FUEL', intoutput-1))
        return int(output)


        pass