## advent of code 2021
## https://adventofcode.com/2021
## day 18

from aocpuzzle import *

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.snailfish_numbers = lines
        # Tests

        self.test_explode("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]")
        self.test_explode("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]")
        self.test_explode("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]")
        self.test_explode("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
        self.test_explode("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]")
        self.test_split("[10]", "[[5,5]]")
        self.test_split("[11]", "[[5,6]]")
        self.test_magnitude("[[1,2],[[3,4],5]]", 143)
        self.test_magnitude("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384)
        self.test_magnitude("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445)
        self.test_magnitude("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791)
        self.test_magnitude("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137)
        self.test_magnitude("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488)

    def test_explode(self, sn, expected_new_sn):
        res, new_sn = self.check_for_explode(sn)        
        print(sn, " => ", new_sn)
        assert(new_sn == expected_new_sn)
    def test_split(self, sn, expected):
        res, new_sn = self.check_for_split(sn)
        print(sn, " => ", new_sn)
        assert(new_sn == expected)
    def test_magnitude(self, sn, expected):
        res = self.magnitude(sn)
        print(sn, " => ", res)
        assert(res == expected)

    def explode(self, sn, start, end):
        pair = sn[start+1:end]        
        spair = pair.split(",")
        left = int(spair[0])
        right = int(spair[1])
        num_start = None
        num_end = None
        new_sn = ""
        # look left for number
        for i in range(start, -1, -1):
            c = sn[i]
            if c.isdigit():
                if num_start == None:
                    num_start = i
            else:
                if num_start:
                    num_end = i + 1
                    break
        if num_start is not None:
            new_sn = sn[0:num_end]
            num = int(sn[num_end:num_start + 1])
            num += left
            new_sn = new_sn + str(num) + sn[num_start+1:start]
        else:
            new_sn = sn[0:start]
        new_sn = new_sn + "0"
        num_start = None
        num_end = None
        for i in range(end+1, len(sn)):
            c = sn[i]
            if c.isdigit():
                if num_start == None:
                    num_start = i
            else:
                if num_start:
                    num_end = i - 1
                    break
        if num_start is not None:            
            num = int(sn[num_start:num_end + 1])
            num += right
            new_sn = new_sn + sn[end+1:num_start] + str(num) + sn[num_end + 1:]
        else:
            new_sn = new_sn + sn[end+1:]

        return new_sn
                                
    def check_for_explode(self, sn):
        depth = 0
        explode_start = None
        explode_end = None
        for i in range(len(sn)):
            c = sn[i]            
            if c == "[":
                depth += 1                
                if depth == 5:
                    explode_start = i
            elif c == "]":
                if depth == 5:
                    explode_end = i
                    new_str = self.explode(sn, explode_start, explode_end)
                    return True, new_str
                depth -= 1                
        return False, sn
    
    def split(self, sn, start, end):
        num = int(sn[start:end+1])
        left = num // 2
        rm = num % 2
        right = left
        if rm > 0:
            right += 1
        new_sn= sn[:start] + "[" + str(left) + "," + str(right) + "]" + sn[end+1:]
        return new_sn

    def check_for_split(self, sn):
        split_start = None
        split_end = None
        for i in range(len(sn)):
            c = sn[i]
            if c.isdigit():
                if split_start is None:
                    split_start = i
                    split_end = i
                else:                    
                    split_end = i
            else:
                if split_start is not None:
                    if split_end - split_start > 0:
                        new_str = self.split(sn, split_start, split_end)
                        return True, new_str
                split_start = None
        return False, sn


    def reduce(self, sn):
        new_sn = sn
        while(True):
            while(True):
                res, new_sn = self.check_for_explode(new_sn)
                if not res:
                    break
            res, new_sn = self.check_for_split(new_sn)
            if not res:
                break
        return new_sn

    def pair_magnitude(self, sn, start, depth):
        left = None
        right = None
        working_on_right = False
        i = start                
        while(i < len(sn)):
            c = sn[i]                
            if c == "[":
                if not working_on_right:                    
                    left, i = self.pair_magnitude(sn, i+1, depth + 1)
                    
                else:                    
                    right, i = self.pair_magnitude(sn, i+1, depth + 1)
                    
            elif c == ",":
                working_on_right = True                
            elif c == "]":
                break
            elif c.isdigit:
                if not working_on_right:                    
                    left = int(c)
                else:                    
                    right = int(c)
            else:
                assert(False)
            i += 1
        assert(left is not None)
        assert(right is not None)        
        return 3 * left + 2 * right, i

    def magnitude(self, sn):
        res,_ = self.pair_magnitude(sn, 1, 0)
        return res
        

    def add(self, sn1, sn2):
        new_sn = "[" + sn1 + "," + sn2 + "]"
        new_sn = self.reduce(new_sn)
        return new_sn

    def part1(self):
        num = self.snailfish_numbers[0]
        for i in range(1, len(self.snailfish_numbers)):
            num = self.add(num, self.snailfish_numbers[i])            
            
        print(num)
        return self.magnitude(num)

    def part2(self):
        maxmag = 0
        for i in range(len(self.snailfish_numbers)):
            for j in range(len(self.snailfish_numbers)):
                if i == j:
                    continue
                num = self.add(self.snailfish_numbers[i], self.snailfish_numbers[j])
                mag = self.magnitude(num)
                maxmag = max(maxmag, mag)
        return maxmag
