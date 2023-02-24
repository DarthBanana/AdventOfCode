## advent of code 2018
## https://adventofcode.com/2018
## day 07

from collections import deque
import re


rule_re = re.compile(r"Step (\w+) must be finished before step (\w+) can begin")

class Step:
    def __init__(self, name):
        self.name = name
        self.dependent_count = 0
        self.dependents = []

class Puzzle:
    def __init__(self, lines):
        self.rules = []
        self.rule_map = {}
        for line in lines:
            match = rule_re.search(line)
            self.rules.append((match.group(1), match.group(2)))
        for first, second in self.rules:
            step = self.rule_map.get(first, Step(first))
            step.dependents.append(second)
            self.rule_map[first] = step
            step = self.rule_map.get(second, Step(second))
            step.dependent_count += 1           
            self.rule_map[second] = step

    def part1(self):
        unavailable = {}
        steps = []
        available = []
        for step in self.rule_map.values():
            unavailable[step.name] = step.dependent_count
            if step.dependent_count == 0:
                available.append(step.name)
        print(available)
        while available:
            available.sort(reverse=True)        
            next = available.pop()
            steps.append(next)
            for r in self.rule_map[next].dependents:
                count = unavailable[r]
                count -= 1
                unavailable[r] = count
                if count == 0:
                    available.append(r)
        return "".join(steps)




    def part2(self):
        time = 0
        if len(self.rules) > 10:
            worker_count = 5
            min_time = 61
        else:
            worker_count = 2
            min_time = 1
        
        unavailable = {}
        steps = []
        available = []
        busy = []
        for step in self.rule_map.values():
            unavailable[step.name] = step.dependent_count
            if step.dependent_count == 0:
                available.append(step.name)
        target_len = len(self.rule_map.values())
        while len(steps) < target_len:
            available.sort(reverse=True)
            while (len(available) and len(busy) < worker_count):
                next = available.pop()
                duration = (ord(next) - ord('A')) + min_time                
                finished = time + duration
                busy.append((finished, next))                
            
            busy.sort(reverse=True)
            time, next = busy.pop()
            steps.append(next)
            for r in self.rule_map[next].dependents:
                count = unavailable[r]
                count -= 1
                unavailable[r] = count
                if count == 0:
                    available.append(r)
            
        return time