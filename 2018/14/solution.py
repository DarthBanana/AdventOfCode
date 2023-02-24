## advent of code 2018
## https://adventofcode.com/2018
## day 14

class Puzzle:
    def __init__(self, lines):
        self.target_number = int(lines[0])
        self.pattern = []
        for c in lines[0]:
            self.pattern.append(int(c))
            
        self.reset()
    def reset(self):
        #self.recipes = "37"
        self.recipes = [3,7]
        self.elves = [0,1]
        self.pattern_match_count = 0
        self.check_for_pattern = False
    
    def step(self):
        #r0 = int(self.recipes[self.elves[0]])
        #r1 = int(self.recipes[self.elves[1]])
        r0 = self.recipes[self.elves[0]]
        r1 = self.recipes[self.elves[1]]
        score = r0 + r1
        if score > 9:
            self.recipes.append(1)
            if self.is_pattern_match(1):
                return True
            score -= 10
        self.recipes.append(score)
        if self.is_pattern_match(score):
            return True
        #self.recipes = self.recipes + str(score)
        self.elves[0] = (self.elves[0] + 1 + r0) % len(self.recipes)
        self.elves[1] = (self.elves[1] + 1 + r1) % len(self.recipes)
        return False

    def run_steps(self, count):
        while(len(self.recipes) < count):
            self.step()

    def is_pattern_match(self, c):
        if self.check_for_pattern:
            if c == self.pattern[self.pattern_match_count]:
                self.pattern_match_count += 1
                if self.pattern_match_count == len(self.pattern):
                    return True
            else:
                self.pattern_match_count = 0
        return False

    def run_until_pattern(self):
        
        self.check_for_pattern = True        
        for i in range(len(self.recipes)):
            if self.is_pattern_match(self.recipes[i]):
                return i - len(self.pattern)

        while(True):
            if self.step():
                return len(self.recipes) - len(self.pattern)

    def part1(self):
        self.run_steps(self.target_number + 10)
        result = "".join([str(item) for item in self.recipes[self.target_number:self.target_number+10]])
        return result

    def part2(self):
        self.reset()        
        return self.run_until_pattern()
        