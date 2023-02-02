## advent of code 2017
## https://adventofcode.com/2017
## day 19

UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
OPTIONS = {}
OPTIONS[UP] = (LEFT, RIGHT)
OPTIONS[DOWN] = (LEFT, RIGHT)
OPTIONS[LEFT] = (UP, DOWN)
OPTIONS[RIGHT] = (UP, DOWN)


def coord_add(a, b):
    return (a[0] + b[0], a[1] + b[1])


class Puzzle:
    def __init__(self, lines):
        self.valid_path = set()
        self.letters = {}
        self.direction = DOWN
        y = 0
        for line in lines:
            x = 0
            for c in line:
                if not (c == " "):
                    if y == 0:
                        self.start = (x, y)
                    self.valid_path.add((x, y))

                    if c.isalpha():
                        self.letters[(x, y)] = c
                x += 1
            y += 1

    def follow_path(self):
        current = self.start
        direction = DOWN
        string = ""
        self.steps = 1
        while True:
            if current in self.letters.keys():
                string = string + self.letters[current]
            next = coord_add(current, direction)
            if next in self.valid_path:
                current = next
            else:
                found = False
                for dir in OPTIONS[direction]:

                    next = coord_add(current, dir)
                    if next in self.valid_path:
                        direction = dir
                        current = next
                        found = True
                        break
                if not found:
                    return string
            self.steps += 1


def parse_input(lines):
    return Puzzle(lines)


def part1(puzzle):
    print(puzzle.letters)
    print(puzzle.valid_path)
    return puzzle.follow_path()


def part2(puzzle):
    return puzzle.steps
