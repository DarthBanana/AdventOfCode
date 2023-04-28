## advent of code 2021
## https://adventofcode.com/2021
## day 20


from aocpuzzle import *
from PrettyMap2D import *
class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.lookup = lines[0]

        self.reset()


    def reset(self):
        self.image = Map2D(default = '.', lines = self.lines[2:])

    def enhance(self, input):
        if self.lookup[0] != input.default:
            output = Map2D(default = "#")
        else:
            output = Map2D(default = '.')
        tl = input.top_left() - Coord2D(3,3)
        lr = input.bottom_right() + Coord2D(3,3)
        for coord in tl.rectangle_tl_lr_coords(lr):
            value = ""
            for c in coord.rectangle_centered(3,3):
                pixel = input[c]
                if pixel == "#":
                    value += "1"
                else:
                    value += "0"
            index = int(value, 2)
            output[coord] = self.lookup[index]
        return output



    def part1(self):
        self.image.print()
        image = self.enhance(self.image)
        image.print()
        image = self.enhance(image)
        image.print()
        return image.count("#")
        

    def part2(self):
        image = self.image.copy()
        for i in range(50):
            print(i)
            image = self.enhance(image)
        return image.count("#")
        