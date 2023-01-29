## advent of code 2017
## https://adventofcode.com/2017
## day 07

import copy
import re


prog_info_re = re.compile(r"(\w+) \((\d+)\)")
children_re = re.compile(r" -> (.*)$")


class Program:
    def __init__(self, line):
        match = prog_info_re.search(line)
        self.name = match.group(1)
        self.children = []
        self.weight = int(match.group(2))
        self.parent = None
        self.total_weight = 0
        match = children_re.search(line)
        if match:
            self.children = list(match.group(1).split(", "))


class Puzzle:
    def __init__(self, lines):
        self.imbalance = 0
        self.programs = []
        self.prog_map = {}
        for line in lines:
            program = Program(line)
            self.prog_map[program.name] = len(self.programs)
            self.programs.append(Program(line))

    def connect_parents(self):
        for program in self.programs:
            for child in program.children:
                self.programs[self.prog_map[child]].parent = program.name

    def find_oldest_ancestor(self):
        for program in self.programs:
            if program.parent == None:
                return program.name
        assert False

    def find_total_weight(self, name):
        program = self.programs[self.prog_map[name]]
        weight = program.weight
        expected_weight = 0
        child_weights = []
        for child in program.children:
            child_weight = self.find_total_weight(child)
            child_weights.append(child_weight)
            weight += child_weight
        if self.imbalance == 0:
            child_set = set(child_weights)
            if len(child_set) > 1:
                print(child_set)
                assert len(child_set) == 2
                weights = list(child_set)
                a_count = 0
                b_count = 0
                for w in child_weights:
                    if w == weights[0]:
                        a_count += 1
                    else:
                        b_count += 1
                if a_count > b_count:
                    expected = weights[0]
                    wrong = weights[1]
                else:
                    expected = weights[1]
                    wrong = weights[0]
                correction = expected - wrong
                for child in program.children:
                    child_prog = self.programs[self.prog_map[child]]
                    print(child_prog.name, child_prog.total_weight)
                    if child_prog.total_weight == wrong:
                        self.imbalance = child_prog.weight + correction

        program.total_weight = weight
        return weight


def parse_input(lines):
    return Puzzle(lines)


def part1(puzzle):
    puzzle.connect_parents()
    return puzzle.find_oldest_ancestor()


def part2(puzzle):
    root = puzzle.find_oldest_ancestor()
    puzzle.find_total_weight(root)
    return puzzle.imbalance
