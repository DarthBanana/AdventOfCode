## advent of code 2018
## https://adventofcode.com/2018
## day 11

class Puzzle:
    def __init__(self, lines):
        self.sn = int(lines[0])
        self.grid = [[0 for _ in range(301)] for _ in range(301)]
        self.calc_powers()

        self.partial_sums = [[0 for _ in range(301)] for _ in range(301)]
        self.build_partial_sums()
        
    def power(self, x, y):        
        rackID = x + 10
        pl = rackID * y
        pl += self.sn
        pl *= rackID
        pl = pl // 10**2
        pl %= 10
        pl -= 5
        return pl

    
    def calc_partial_sum(self, x,y):
        return self.grid[x][y] + self.partial_sums[x-1][y] + self.partial_sums[x][y-1] - self.partial_sums[x-1][y-1]
    def calc_powers(self):
        for x in range(1, 301):
            for y in range(1, 301):
                self.grid[x][y] = self.power(x,y)

    def build_partial_sums(self):
        for y in range(1, 301):
            for x in range(1, 301):
                self.partial_sums[x][y] = self.calc_partial_sum(x,y)

    def max_for_width(self, width):
        ans = (0, (0, 0))
        for x in range(1, 301-width):
            for y in range(1, 301-width):
                tot  = self.partial_sums[x+width][y+width] - self.partial_sums[x][y+width] - self.partial_sums[x+width][y] + self.partial_sums[x][y]
                ans = max(ans, (tot, (x+1, y+1)))
        return ans

    def part1(self):
        
        maximum, (x,y) = self.max_for_width(3)
        return "{},{}".format(x, y)

    def part2(self):
        results = {}
        
        for width in range(3,300):
            #print(width)
            maximum, (x,y) = self.max_for_width(width)
            results[maximum] = (x,y,width)
        x,y,width = results[max(results)]
        
        return "{},{},{}".format(x, y, width)

        