## advent of code 2021
## https://adventofcode.com/2021
## day 16

from aocpuzzle import *
from operator import mul
from functools import reduce
class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.hex_string = self.lines[0]
        self.binary_string = self.hex_to_binary(self.hex_string)
        #print(self.hex_string)
        #print(self.binary_string)
        self.version_sum = 0

    def hex_to_binary(self, hex_string):
        return bin(int(hex_string, 16))[2:].zfill(len(hex_string) * 4)
    
    def parse_packet(self, binary_string):
        result = 0
        #print(binary_string)
        version_string = binary_string[0:3]
        #print(version_string)
        version = int(version_string, 2)
        self.version_sum += version
        type_string = binary_string[3:6]
        type_id = int(type_string, 2)
        #print(version, type_id)
        offset = 6
        if type_id == 4:

            # literal value
            literal_string = ""
            while True:
                c = binary_string[offset]
                #print(c)
                offset += 1
                value = binary_string[offset:offset + 4]
                #print("hex char: ", value)
                literal_string = literal_string + value

                offset += 4
                if c == "0":
                    result = int(literal_string,2)
                    break
            
        else:
            values = []            
            length_type = binary_string[offset]
            offset += 1
            if length_type == "0":
                length = int(binary_string[offset:offset + 15],2)
                offset += 15
                end = offset + length
                while (offset < end):
                    packet_size, value = self.parse_packet(binary_string[offset:])
                    values.append(value)
                    offset += packet_size
            else:
                count = int(binary_string[offset:offset + 11], 2)
                offset += 11
                for i in range(count):
                    packet_size, value = self.parse_packet(binary_string[offset:])
                    values.append(value)
                    offset += packet_size
            #print("values: ", values)
            if type_id == 0:
                result = sum(values)
            elif type_id == 1:
                result = reduce(mul, values, 1)
            elif type_id == 2:
                result = min(values)
            elif type_id == 3:
                result = max(values)
            elif type_id == 5:
                if values[0] > values[1]:
                    result = 1
            elif type_id == 6:
                if values[0] < values[1]:
                    result = 1                
            elif type_id == 7:
                if values[0] == values[1]:
                    result = 1

        return offset, result
            
        
        


    def part1(self):
        offset, result = self.parse_packet(self.binary_string)
        return self.version_sum

    def part2(self):
        offset, result = self.parse_packet(self.binary_string)
        return result