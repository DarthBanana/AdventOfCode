## advent of code 2021
## https://adventofcode.com/2021
## day 04


from aocpuzzle import *
from parsehelp import *

class Board:    
    def __init__(self, lines, id):
        self.id = id
        print(self.id)
        self.numbers = {}
        for r in range(5):
            row = get_all_ints(lines[r])
            for c in range(5):
                val = row[c]
                self.numbers[val] = (r, c)        
        self.reset()
    
    def reset(self):
        self.rows = [0 for i in range(5)]
        self.cols = [0 for i in range(5)]
        self.won = False
        self.sum_total = sum(self.numbers.keys())
    
    def call_number(self, number):
        if number in self.numbers:
            self.sum_total -= number
            r, c = self.numbers[number]
            self.rows[r] += 1
            if self.rows[r] >= 5:
                self.won = True
            self.cols[c] += 1
            if self.cols[c] >= 5:
                self.won = True
            


class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):        
        AoCPuzzle.__init__(self, lines, is_test)
        self.numbers = get_all_ints(lines[0])
        self.boards = []
        id = 0
        for i in range(2, len(self.lines), 6):
            
            self.boards.append(Board(self.lines[i:i+5], id))
            id += 1

    def play_game(self, find_loser=False):
        for n in self.numbers:
            
            for b in self.boards:
                b.call_number(n)
                if b.won:
                    return b.sum_total * n
                    
    def play_game_loser(self):
        for b in self.boards:
            b.reset()
        finished_boards = []        
        winners = 0
        for n in self.numbers:            
            for b in self.boards:                
                if b.id in finished_boards:                    
                    continue
                
                b.call_number(n)
                if b.won:
                    winners += 1
                    finished_boards.append(b.id)
                    if len(finished_boards) == len(self.boards):
                        return b.sum_total * n

    def part1(self):
        return self.play_game()
        

    def part2(self):
        return self.play_game_loser()
        pass