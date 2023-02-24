## advent of code 2018
## https://adventofcode.com/2018
## day 01
import sys
sys.path.insert(0, "d:\\git\\AdventOfCode\\2018\\MyModules")
import parsehelp

def parse_input(lines):
    return parsehelp.get_list_of_int_per_line(lines)
    

def part1(data):
    value = 0
    for num in data:
        value += num
    return value

def part2(data):
    value = 0
    history = set()
    index = 0
    while not (value in history):
        history.add(value)
        value += data[index]
        index = (index + 1) % len(data)
    return value
