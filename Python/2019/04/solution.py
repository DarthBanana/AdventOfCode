## advent of code 2019
## https://adventofcode.com/2019
## day 04

from aocpuzzle import *

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        input = lines[0].split('-')
        self.min_value = int(input[0])
        self.min_digits = [int(x) for x in input[0]]
        self.max_value = int(input[1])
        self.max_digits = [int(x) for x in input[1]]
        self.valid_passwords = []

    def next_digit(self, pair, digits_left, value, last_digit):
        #print(pair, digits_left, value, last_digit)        
        
        start_value = last_digit
        if value < self.min_value:
            start_value = max(last_digit, self.min_digits[len(self.min_digits)-digits_left])
        digits_left -= 1
        my_multiplier = 10**digits_left
        for d in range(start_value, 10):
            my_pair = pair
            if d == last_digit:
                my_pair = True
            my_value = value+ d * my_multiplier
            #print("my_value:", my_value)
            if digits_left:
                if (self.next_digit(my_pair, digits_left, my_value, d)):
                    return True
            else:
                if my_value < self.min_value:
                    #print(my_value, self.min_value)
                    assert(False)
                if my_value > self.max_value:
                    return True
                if my_pair == False:
                    continue
                self.valid_passwords.append(my_value)
                #print(my_value)                
            
        return False
        
    def test_value2(self, value):
        if value < self.min_value:
            return False
        if value > self.max_value:
            return False
        
        value_string = str(value)
        if not (len(value_string) == 6):
            return False
        
        digits = [int(x) for x in value_string]
        last_d = 0
        streak_len = 0
        pair_found = False
        for d in digits:
            if d < last_d:
                return False
            if d > last_d:
                if streak_len == 2:
                    pair_found = True
                streak_len = 1
            if d == last_d:
                streak_len += 1
            last_d = d
        if streak_len == 2:
            pair_found = True
        if pair_found:
            return True
        return False


    
    def next_digit2(self, streak_count, pair, digits_left, value, last_digit):
        #print(pair, digits_left, value, last_digit)  
              
        if not digits_left:
            if streak_count == 2:
                pair = True
            if value < self.min_value:
                assert(False)
            if value > self.max_value:
                return True
            if pair == False:
                return False
            self.valid_passwords.append(value)                  
            return False
        
                    
        start_value = last_digit
        if value < self.min_value:
            start_value = max(last_digit, self.min_digits[len(self.min_digits)-digits_left])
        digits_left -= 1
        my_multiplier = 10**digits_left
        for d in range(start_value, 10):
            
            my_pair = pair
            if d == last_digit:
                my_streak_count = streak_count + 1                                
            else:
                if streak_count == 2:                    
                    my_pair = True
                my_streak_count = 1                

            my_value = value+ d * my_multiplier
            #print("my_value:", my_value)
            if (self.next_digit2(my_streak_count, my_pair, digits_left, my_value, d)):
                return True
            
        return False
    
    def part1(self):
        self.next_digit(False, 6, 0, 0)
        #print(self.valid_passwords)
        return len(self.valid_passwords)
    
    def part2a(self):
        my_test_results = []
        for i in range(self.min_value, self.max_value + 1):
            if self.test_value2(i):
                my_test_results.append(i)
        return my_test_results
    
    def part2b(self):
        self.valid_passwords = []
        self.next_digit2(0, False, 6, 0, 0)
        return self.valid_passwords
    
    def part2(self):
        #pwds = self.part2a()
        pwds = self.part2b()
        return len(pwds)