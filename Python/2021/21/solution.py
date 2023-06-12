## advent of code 2021
## https://adventofcode.com/2021
## day 21

rolls = [0,0,0,1,3,6,7,3,1]
#111 = 3
#112 = 4
#113 = 5
#121 = 4
#122 = 5
#123 = 6
#131 = 5
#132 = 6
#133 = 7
#211 = 4
#212 = 5
#213 = 6
#221 = 5
#222 = 6
#223 = 7
#231 = 6
#232 = 7
#233 = 8
#311 = 5     
#312 = 6
#313 = 7
#321 = 6
#322 = 7
#323 = 8
#331 = 7
#332 = 8
#333 = 9
from collections import defaultdict
from aocpuzzle import *
class Die:
    def __init__(self, deterministic = False):
        self.deterministic = deterministic
        self.sides = 100
        self.value = 1
        self.rolls = 0

    def roll(self):
        value = 0
        self.rolls += 1
        if self.deterministic:
            value = self.value
            self.value += 1
            self.value % self.sides
        return value
    
class Player:
    def __init__(self, id, starting_pos):
        
        self.id = id
        self.start_pos = starting_pos
        self.reset()

    def reset(self):
        self.pos = self.start_pos - 1
        self.score = 0
        self.wins = defaultdict(lambda : 0)
        self.scenarios = defaultdict(lambda : 0)
        self.scenarios[(0, self.start_pos)] = 1
        self.wins_per_round = 0

    def take_turn(self, die):
        roll1 = die.roll()
        roll2 = die.roll()
        roll3 = die.roll()
        total = roll1 + roll2 + roll3
        self.pos += total
        self.pos %= 10        
        self.score += self.pos + 1
        #print("Player ", self.id, " rolled ", roll1, roll2, roll3, " for ", total, " and is now at ", self.pos + 1, " with score ", self.score)
    def get_total(self):
        return sum(self.scenarios.values())
    
    def take_qantum_turn(self):
        new_scenarios = defaultdict(lambda : 0)
        min_score = 21
        wins = 0
        for r in range(len(rolls)):
            if r == 0:
                continue

            for s, c in self.scenarios.items():
                score, pos = s
                new_pos = (pos + r) % 10
                new_score = score + new_pos + 1
                num_games_in_state = c * rolls[r]
                min_score = min(min_score, new_score)
                if new_score >= 21:
                    wins += c * rolls[r]
                else:
                    new_scenarios[(new_score, new_pos)] += (c * rolls[r])
        
        
        print(min_score)
        self.scenarios = new_scenarios
        return wins

    def play_all_games(self):
        turn = 0
        while len(self.scenarios) > 0:
            turn += 1
            print(turn, len(self.scenarios))
            wins = self.take_qantum_turn()
            self.wins[turn] = wins
        return turn



class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.players = []
        for line in lines:
            nums = get_all_ints(line)
        
            player = Player(nums[0], nums[1])
            self.players.append(player)
        self.reset()
    
    def reset(self):
        for player in self.players:
            player.reset()

    def play_game(self, die):
        turn = 0
        while True:
            player = turn % len(self.players)
            turn += 1
            self.players[player].take_turn(die)
            if self.players[player].score >= 1000:
                return player

    def part1(self):
        die = Die(deterministic=True)
        winner = self.play_game(die)
        loser_score = 0
        if winner == 0:
            loser_score = self.players[1].score
        else:
            loser_score = self.players[0].score
        print(self.players[0].score, self.players[1].score, die.rolls)
        return loser_score * die.rolls

    def play_game2(self):
        turn = 0
        other_wins = 0
        for p in self.players:
            p.play_all_games()
        
        prod = 1
        total_p1_wins = 0
        for i in range(1, len(self.players[0].wins)+1):
            total_p1_wins += self.players[0].wins[i] * prod
            prod *= 27
            prod -= self.players[1].wins[i]
        total_p2_wins = 0
        prod = 1
        for i in range(1, len(self.players[1].wins)+1):
            total_p2_wins += self.players[1].wins[i] * prod
            prod *= 27
            prod -= self.players[0].wins[i]
        print(total_p1_wins, total_p2_wins)
        return max(total_p1_wins, total_p2_wins)

    def part2(self):
        self.reset()
        return self.play_game2()
        

        wins = [p.wins for p in self.players]
        print(wins)
        return max(wins)

            
        pass