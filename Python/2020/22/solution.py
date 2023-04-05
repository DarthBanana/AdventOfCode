## advent of code 2020
## https://adventofcode.com/2020
## day 22

from collections import deque
from aocpuzzle import *
from itertools import islice

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.player1 = deque()
        self.player2 = deque()
        for line in lines:
            if line.startswith('Player 1'):
                player = self.player1
            elif line.startswith('Player 2'):
                player = self.player2
            elif line:
                player.append(int(line))
        self.history = {}
        
    def play_round(self, player1, player2):
        card1 = player1.popleft()
        card2 = player2.popleft()
        if card1 > card2:
            player1.append(card1)
            player1.append(card2)
        else:
            player2.append(card2)
            player2.append(card1)

    def play_game(self, player1, player2):
        while player1 and player2:
            self.play_round(player1, player2)
        return player1, player2
   
    def play_recursive_game(self, player1, player2, level=1):        
                
        history1 = set()   
        history2 = set()
        round = 0     
        while(player1 and player2):
            round += 1

            hash1 = tuple(player1)
            hash2 = tuple(player2)
            if hash1 in history1 and hash2 in history2:
                return player1, None
            history1.add(hash1)
            history2.add(hash2)
                        
            card1 = player1.popleft()
            card2 = player2.popleft()

            if (len(player1) >= card1) and (len(player2) >= card2):
                p1, p2 = self.play_recursive_game(deque(list(player1)[:card1]), deque(list(player2)[:card2]), level+1)
                if p1:
                    winner = 1
                else:
                    winner = 2
            else:
                if card1 > card2:
                    winner = 1
                else:
                    winner = 2
            if winner == 1:
                player1.append(card1)
                player1.append(card2)
            else:
                player2.append(card2)
                player2.append(card1)
        return player1, player2

    def calculate_winner_score(self, player1, player2):
        winner = player1 if player1 else player2
        score = 0
        for i, card in enumerate(reversed(winner)):
            score += (i+1) * card
        return score
    def part1(self):
        player1, player2 = self.play_game(self.player1.copy(), self.player2.copy())
        return self.calculate_winner_score(player1, player2)

    def part2(self):
        player1, player2 = self.play_recursive_game(self.player1.copy(), self.player2.copy())

        return self.calculate_winner_score(player1, player2)
    
        pass