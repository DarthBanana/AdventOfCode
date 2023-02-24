## advent of code 2018
## https://adventofcode.com/2018
## day 02

import re



def parse_input(lines):

    return lines

def part1(data):
    twos = 0
    threes = 0
    for word in data:
        map = {}
        for c in word:
            map[c] = map.get(c, 0) + 1
        if 2 in map.values():
            twos += 1
        if 3 in map.values():
            threes += 1
    

    return twos * threes

def overlap(worda, wordb):
    shared = "".join(a for a,b in zip(worda, wordb) if a == b)
    return shared
    

def part2(data):
    while len(data) > 1:
        a = data.pop()
        for b in data:
            ol = overlap(a,b)
            if len(ol) == len(a) - 1:
                return ol

