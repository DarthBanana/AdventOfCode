## advent of code 2018
## https://adventofcode.com/2018
## day 08

from collections import deque
from parsehelp import *

class Node:
    def __init__(self, numbers):
        self.num_children = numbers.popleft()
        self.num_metadata = numbers.popleft()
        self.children = []
        self.metadata = []
        for i in range(self.num_children):
            self.children.append(Node(numbers))
        for i in range(self.num_metadata):
            self.metadata.append(numbers.popleft())
    def add_metadata(self):
        sum = 0
        for c in self.children:
            sum += c.add_metadata()
        for m in self.metadata:
            sum += m
        return sum

    def get_value(self):
        if len(self.children) == 0:
            return sum(self.metadata)
        value = 0
        for m in self.metadata:
            
            if 0 < m <= len(self.children):
                value += self.children[m - 1].get_value()
            
        return value


class Puzzle:
    def __init__(self, lines):
        self.numbers = deque(get_ints_per_line(lines))           
        self.root_node = Node(self.numbers)
    
    def part1(self):
        return self.root_node.add_metadata()

    def part2(self):
        return self.root_node.get_value()