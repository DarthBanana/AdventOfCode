## advent of code 2020
## https://adventofcode.com/2020
## day 14

from aocpuzzle import *
from parsehelp import *

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.reset()
    def reset(self):
        self.data = {}
        self.mask = None

    def apply_mask(self, value):
        value = list(bin(value)[2:].zfill(36))
        for i, bit in enumerate(self.mask):
            if bit != 'X':
                value[i] = bit
        return int(''.join(value), 2)
    
    def write_masked_address(self, address, value):
        address = list(bin(address)[2:].zfill(36))
        addresses = []
        for i, bit in enumerate(self.mask):
            if bit == '1':
                address[i] = '1'
            elif bit == 'X':
                address[i] = 'X'
        addresses.append(''.join(address))
        while 'X' in addresses[0]:
            new_addresses = []
            for address in addresses:
                new_addresses.append(address.replace('X', '0', 1))
                new_addresses.append(address.replace('X', '1', 1))
            addresses = new_addresses
        for address in addresses:
            self.data[int(address, 2)] = value
    
    def run_instructions(self):
        for line in self.lines:
            if line.startswith('mask'):
                self.mask = line.split(' = ')[1]
            else:
                nums = get_all_ints(line)
                address = nums[0]
                value = nums[1]                
                self.data[address] = self.apply_mask(value)

    def run_instructions2(self):
        for line in self.lines:
            if line.startswith('mask'):
                self.mask = line.split(' = ')[1]
            else:
                nums = get_all_ints(line)
                address = nums[0]
                value = nums[1]    
                self.write_masked_address(address, value)
                
    def part1(self):
        self.reset()
        self.run_instructions()
        return sum(self.data.values())

    def part2(self):
        self.reset()
        self.run_instructions2()
        return sum(self.data.values())