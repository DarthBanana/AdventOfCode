## advent of code 2021
## https://adventofcode.com/2021
## day 08

from aocpuzzle import *
PATTERNS = [set(list("abcefg")), set(list("cf")), set(list("acdeg")), set(list("acdfg")), set(list("bcdf")), set(list("abdfg")), set(list("abdefg")), set(list("acf")), set(list("abcdefg")), set(list("abcdfg"))]
CANDIDATES = {
    2: [1],
    3: [7],
    4: [4],
    5: [2, 3, 5],
    6: [0, 6, 9],
    7: [8]
}
class Notes:
    def __init__(self, line):
        input, output = line.split(' | ')
        input = input.split()
        self.input = [set(list(w)) for w in input]
        output = output.split()
        self.output = [set(list(w)) for w in output]
        self.mapping = {}
        for c in PATTERNS[8]:
            self.mapping[c] = PATTERNS[8]        
    
    def get_digits(self, input):
        return CANDIDATES[len(input)]

    def get_digit(self, output):
        segments = set()
        for o in output:
            segments.add(self.mapping[o])
        return PATTERNS.index(segments)
    
    def get_digits(self):
        total = 0
        for o in self.output:
            total = total * 10 + self.get_digit(o)
        return total

        
    def determine_mapping(self):       
        len_map = {}

        for i in self.input:
            length = len(i)
            if length in len_map:
                len_map[length].append(i)
            else:
                len_map[length] = [i]        
        digit_1 = len_map[2][0]
        digit_7 = len_map[3][0]
        digit_4 = len_map[4][0]
        digit_8 = len_map[7][0]
        digit_0 = None
        digit_2 = None
        digit_3 = None
        digit_5 = None
        digit_6 = None
        digit_9 = None

        a = digit_7 - digit_1        
        cf = digit_1
        bd = digit_4 - digit_1
        eg = (digit_8 - digit_4) - digit_7
        #print("a:", a)
        #print("cf:", cf)
        #print("bd:", bd)
        #print("eg:", eg)
        for i in len_map[6]:
            diff = (digit_8 - i).pop()
            #print(i, diff)
            if diff in bd:
                digit_0 = i
            elif diff in cf:
                digit_6 = i
            else:
                digit_9 = i
        #print("0 = ", digit_0)
        #print("6 = ", digit_6)
        #print("9 = ", digit_9)
        for i in len_map[5]:
            if cf in i:
                digit_3 = i
            elif len(digit_6 - i) == 1:
                digit_5 = i
            else:
                digit_2 = i
        
        e = digit_6 - digit_5
        g = eg - e
        d = digit_8 - digit_0
        b = bd - d
        c = digit_8 - digit_6
        f = cf - c
        a = a.pop()
        b = b.pop()
        c = c.pop()
        d = d.pop()
        e = e.pop()
        f = f.pop()
        g = g.pop()
        self.mapping[a] = "a"
        self.mapping[b] = "b"
        self.mapping[c] = "c"
        self.mapping[d] = "d"
        self.mapping[e] = "e"
        self.mapping[f] = "f"
        self.mapping[g] = "g"         


        
class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.notes = []
        for line in lines:
            self.notes.append(Notes(line))
        

    def part1(self):
        count = 0
        for n in self.notes:
            for o in n.output:
                l = len(o)
                if l == 2 or l == 4 or l == 3 or l == 7:
                    count += 1
        return count

    def part2(self):
        total = 0
        for n in self.notes:
            n.determine_mapping()
            total += n.get_digits()
        return total