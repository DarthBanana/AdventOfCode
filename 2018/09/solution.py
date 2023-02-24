## advent of code 2018
## https://adventofcode.com/2018
## day 09
from collections import deque
import re
from RingList import *


puzzle_re = re.compile(r"(\d+) players; last marble is worth (\d+) points")
result_re = re.compile(r"high score is (\d+)")
class Puzzle:
    def __init__(self, lines):
        self.runs = []
        self.solutions = []
        for line in lines:
            match = puzzle_re.search(line)
            self.runs.append((int(match.group(1)), int(match.group(2))))
            match = result_re.search(line)
            if match:
                self.solutions.append(int(match.group(1)))
            else:
                self.solutions.append(None)        

    def print(first, cur):
        c = first
        while True:
            if c == cur:
                print(" (",c.data,") ", end="")
            else:
                print("  ",c.data, "  ", end="")
            c = c.next
            if c == first:
                print()
                return
        
    def play2(self, players, last):
        ring = deque()    
        ring.append(0)
        scores = [0 for i in range(players)]
        player = 0
        for i in range(1, last+1):
            if (i % 23 == 0):
                scores[player] += i
                ring.rotate(7)
                other = ring.pop()
                ring.rotate(-1)
                scores[player] += other
            else:
                ring.rotate(-1)
                ring.append(i)
            player = (player+1)%players
        return max(scores)

    def play(self, players, last):
        first = RingNode(0)
        scores = [0 for i in range(players)]
        cur = first
        player = 0
        for i in range(1, last+1):
            if (i % 23 == 0):
                scores[player] += i
                other = cur.get_n_back(7)
                other.remove()
                cur = cur.get_n_back(6)
                scores[player] += other.data
            else:
                new = RingNode(i)
                cur = cur.get_n_forward(1)
                cur.insert_after(new)
                cur = new
            player = (player + 1) % players
        return max(scores)

    def part1(self):
        for i in range(len(self.runs)):
            run = self.runs[i]   
            print(run)     
            result = self.play2(run[0], run[1])
            print("  ", result)
            if self.solutions[i]:
                assert(self.solutions[i] == result)
            else:
                return result

    def part2(self):
        run = self.runs[0]
        print(run)
        result = self.play2(run[0], run[1]*100)
        print("  ", result)
        return result