## advent of code 2021
## https://adventofcode.com/2021
## day 10

from aocpuzzle import *

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)

    def point_value(self, c):
        if c == ")":
            return 3
        elif c == "]":
            return 57
        elif c == "}":
            return 1197
        elif c == ">":
            return 25137
        return 0
    
    def remainder_point_value(self,remainder):
        score = 0
        for c in remainder:
            score *= 5
            if c == ")":
                score += 1
            elif c == "]":
                score += 2
            elif c == "}":
                score += 3
            elif c == ">":
                score += 4
        return score
    def get_match(self, c):
        if c == "(":
            return ")"
        if c == "[":
            return "]"
        if c == "{":
            return "}"
        if c == "<":
            return ">"
        assert(False)

    def parse_chunk(self, string, index = 0):
        c = None
        while index < len(string):
            c = string[index]            
            if c == "(" or c == "[" or c == "{" or c == "<":                
                result, index, remainder = self.parse_chunk(string, index+1)
                if not result:
                    return result, index, None
                if index >= len(string):
                    remainder = remainder + self.get_match(c)
                    return True, index, remainder
                assert(index < len(string))
                d = string[index]
                if d == self.get_match(c):
                    index += 1                
                else:                    
                    return False, index, None
            else:                
                return True, index, None
        
        return True, index, ""
    
    def part1(self):
        score = 0
        for line in self.lines:
            result, index, remainder = self.parse_chunk(line)
            if not result:
                #print("FAILURE")
                c = line[index]
                #print(c)
                score += self.point_value(c)
            else:
                print(remainder)


        return score

    def part2(self):
        scores = []
        for line in self.lines:
            result, index, remainder = self.parse_chunk(line)
            if result:
                
                score = self.remainder_point_value(remainder)
                print(remainder, score)
                scores.append(score)
        
        scores.sort()
        index = len(scores)//2
        return scores[index]
        