## advent of code 2020
## https://adventofcode.com/2020
## day 21

from aocpuzzle import *

class Food:
    def __init__(self, line):
        self.line = line
        ingredients, allergens = line.split(' (contains ')
        self.ingredients = ingredients.split()
        for i in range(len(self.ingredients)):
            self.ingredients[i] = self.ingredients[i].strip()
        self.allergens = allergens[:-1].split(', ')
        for i in range(len(self.allergens)):
            self.allergens[i] = self.allergens[i].strip()
        
        assert(len(self.ingredients) == len(set(self.ingredients)))

    def __str__(self):
        return self.line
    def __repr__(self):
        return self.line
    
class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.ingredients = set()
        self.alergens = {}
        self.foods = []
        self.safe = set()
        for line in lines:
            food = Food(line)
            self.foods.append(food)
            self.ingredients.update(food.ingredients)
            for alergen in food.allergens:
                if alergen in self.alergens:
                    self.alergens[alergen].intersection_update(food.ingredients)
                else:
                    self.alergens[alergen] = set(food.ingredients)
        self.safe = self.ingredients.copy()
        for alergen, ingredients in self.alergens.items():
            self.safe.difference_update(ingredients)


    def part1(self):
        count = 0
        print(self.alergens)
        print(self.safe)
        for food in self.foods:
            count += len(set(food.ingredients) & self.safe)

        return count

    def part2(self):
        unknown_alergens = set(self.alergens.keys())
        known_alergens = {}
        while len(unknown_alergens) > 0:
            for alergen, ingredients in self.alergens.items():
                if len(ingredients) == 1:
                    known_alergens[alergen] = ingredients.pop()
                    unknown_alergens.remove(alergen)
                    for alergen2, ingredients2 in self.alergens.items():
                        ingredients2.discard(known_alergens[alergen])
                    break
        return ','.join([known_alergens[alergen] for alergen in sorted(known_alergens.keys())])