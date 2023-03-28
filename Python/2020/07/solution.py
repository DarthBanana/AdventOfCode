## advent of code 2020
## https://adventofcode.com/2020
## day 07

from aocpuzzle import *

class Rule:
    def __init__(self, line):
        self.bag = line.split(' bags contain ')[0]
        self.contains = []
        for rule in line.split(' bags contain ')[1].split(', '):
            if rule == 'no other bags.':
                continue
            splitrule = rule.split(' ')
            self.contains.append((int(splitrule[0]), splitrule[1] + ' ' + splitrule[2]))

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.rules = []
        for line in lines:
            self.rules.append(Rule(line))

    def contains_bag(self, bag):
        bags = []
        for rule in self.rules:            
            for b in rule.contains:                
                if b[1] == bag:                    
                    bags.append(rule.bag)
        return bags

    def part1(self):
        starting_bag = 'shiny gold'
        bags_to_check = [starting_bag]
        bags = []
        while len(bags_to_check) > 0:
            bag = bags_to_check.pop()
            contains = self.contains_bag(bag)
            bags_to_check += contains
            bags += contains            

        return len(set(bags))

    def count_bags(self, bag):
        count = 0
        for rule in self.rules:
            if rule.bag == bag:
                for b in rule.contains:
                    count += b[0] * (1 + self.count_bags(b[1]))
        return count

    def part2(self):
        starting_bag = 'shiny gold'
        return self.count_bags(starting_bag)