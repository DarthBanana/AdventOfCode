## advent of code 2020
## https://adventofcode.com/2020
## day 19

import copy
import re
from aocpuzzle import *
from parsehelp import *

direct_rule = re.compile(r'(\d+): "(\w)"')
class Rule:
    def __init__(self, line):
        self.value = None
        self.dependencies = []
        match = direct_rule.match(line)
        if match:
            self.id = int(match.group(1))
            self.value = match.group(2)
            return
        
        self.compiled = []
        

        self.id, rule = line.split(': ')
        self.id = int(self.id)        
        rule = rule.split(' | ')
        self.compiled_rules = {}
        for r in rule:            
            self.dependencies.append(get_all_ints(r))
    def __str__(self):
        if self.value != None:
            return f'{self.id}: \"{self.value}\"'
        else:
            return f'{self.id}: {self.dependencies}'
    def __repr__(self):
        return self.__str__()

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.rules = {}
        self.messages = []
        for line in lines:
            if ':' in line:
                rule = Rule(line)
                self.rules[rule.id] = rule
            elif len(line):
                self.messages.append(line)

    def is_match(self, message, rule, start=0):
        #print(rule.id, message, start, rule.value, rule.dependencies)
        if rule.value:
            index = message.find(rule.value, start)
            if index != start:
                return False, start
            return True, index + 1
        best = 100000000
        found_match = False
        for dependency in rule.dependencies:
            index = start            
            for r in dependency:
                match, index = self.is_match(message, self.rules[r], index)
                if not match:
                    break
            if match:
                assert(found_match == False)
                found_match = True
                best = min(best, index)
        return found_match, best
    
    def find_matches(self, message, rule, start=0):        
        if rule.value:            
            match = re.match(rule.value, message[start:])
            if match:
                return [start + len(match.group(0))]
            return []
        
        matches = []
        for dependency in rule.dependencies:
            indexes = [start]            
            
            for r in dependency:                
                if isinstance(r, str):
                    new_indexes = []                    
                    for index in indexes:
                        match = re.match(r, message[index:])
                        if match:
                            new_indexes.append(index + len(match.group(0)))
                    indexes = new_indexes
                else:
                    new_indexes = []
                    for index in indexes:
                        new_indexes += self.find_matches(message, self.compiled_rules[r], index)
                    indexes = new_indexes
                if not len(indexes):
                    break
            if len(indexes):
                matches += indexes
        return matches        


    def add_used(self, id, used):
        rule = self.compiled_rules[id]
        used.add(rule.id)
        for d in rule.dependencies:
            for i in d:
                if isinstance(i, int):
                    if i in used:
                        continue                    
                    used = self.add_used(i, used)
        return used
    
    def remove_unused(self):
        used = set()
        used = self.add_used(0, used)        
        for id in list(self.compiled_rules.keys()):
            if id not in used:
                del self.compiled_rules[id]

    def sort_dependencies(self):
        for r in self.compiled_rules.values():
            const_deps = []
            var_deps = []
            for d in r.dependencies:
                var = False
                var_index = -1
                for i in range(len(d)):
                    if isinstance(d[i], int):
                        var = True
                        var_index = i
                        break
                if var:
                    var_deps.append((d, var_index))
                else:
                    const_deps.append(d)
            var_deps.sort(key=lambda x: x[1])
            var_deps = [x[0] for x in var_deps]            
            r.dependencies = const_deps + var_deps                    
            
                
    def remove_consts(self):
        found = False
        
        value_rules = []
        for r in self.compiled_rules.values():
            if r.value:
                value_rules.append(r)                
                for o in self.compiled_rules.values():
                    if o.value:
                        continue
                    for d in o.dependencies:
                        for i in range(len(d)):
                            if d[i] == r.id:
                                d[i] = r.value
                        
        for r in value_rules:
            if r.id == 0:
                continue
            found = True            
            del self.compiled_rules[r.id]
        return found
    
    def reduce(self):
        found = False
        for r in self.compiled_rules.values():
            can_be_removed = True
            if r.value:
                continue
            assert(r.value == None)
            for j in range(len(r.dependencies)):
                d = r.dependencies[j]
                can_be_reduced = True
                for i in range(len(d)):
                    if isinstance(d[i], int):
                        can_be_reduced = False
                        can_be_removed = False
                        break
                if can_be_reduced:                    
                    d = ''.join(d)
                    r.dependencies[j] = [d]
            if can_be_removed:                                
                found = True
                if len(r.dependencies) == 1:
                    r.value = r.dependencies[0][0]
                    r.dependencies = []
                    continue
                r.value = "("
                for d in r.dependencies:                    
                    r.value += d[0]
                    r.value += "|"
                r.value = r.value[:-1]
                r.value += ")"
                r.dependencies = []                
        return found
    
    def compile(self):
        self.compiled_rules = copy.deepcopy(self.rules)
        while self.remove_consts() == True:
            self.reduce()
        self.remove_unused()
        self.sort_dependencies()

                

    def print_rules(self, rules):
        ids = list(rules.keys())
        ids.sort()
        for i in ids:
            print(rules[i])

    def part1(self):
        self.compile()
        count = 0
        for message in self.messages:
            matches = self.find_matches(message, self.compiled_rules[0])
            if len(message) in matches:
                count += 1
                #print(message)
        return count

    def part2(self):
        
        self.rules[8] = Rule('8: 42 | 42 8')
        self.rules[11] = Rule('11: 42 31 | 42 11 31')
        
        self.compile()
        count = 0
        for message in self.messages:
            matches = self.find_matches(message, self.compiled_rules[0])
            if len(message) in matches:
                count += 1
                #print(message)
        return count