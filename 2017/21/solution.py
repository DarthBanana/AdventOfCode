## advent of code 2017
## https://adventofcode.com/2017
## day 21
import numpy as np


def add_em(a, b):
    return tuple(x + y for x, y in zip(a, b))


class Grid:
    def __init__(self, size):
        self.values = {}
        self.size = size
        if size % 2 == 0:
            self.tile_size = 2
            self.next_size = int(3 * size / 2)
        else:
            self.tile_size = 3
            self.next_size = int(4 * size / 3)

    def print(self):
        print("Printing")

        for y in range(self.size):
            for x in range(self.size):
                print(self.values[(x, y)], end="")
            print()

    def set_start(self):
        t = [[".", "#", "."], [".", ".", "#"], ["#", "#", "#"]]
        for y in range(3):
            for x in range(3):
                self.values[(x, y)] = t[y][x]

    def get_tile(self, tlx, tly):
        tile = ""
        for y in range(tly, tly + self.tile_size):
            for x in range(tlx, tlx + self.tile_size):
                tile = tile + self.values[(x, y)]
        return tile

    def get_tile_iter(self):
        index = 0

        for y in range(0, self.size, self.tile_size):
            for x in range(0, self.size, self.tile_size):
                yield (index, self.get_tile(x, y))
                index += 1

    def set_tile(self, index, tile):
        if len(tile) == 9:
            tile_size = 3
        else:
            tile_size = 4

        tiles_per_row = self.size / tile_size
        row = int(index / tiles_per_row)
        col = int(index % tiles_per_row)
        tlx = int(col * tile_size)
        tly = int(row * tile_size)
        index = 0

        for y in range(tly, tly + tile_size):
            for x in range(tlx, tlx + tile_size):
                self.values[(x, y)] = tile[index]
                index += 1

    def count_ons(self):
        count = 0
        for v in self.values.values():
            if v == "#":
                count += 1
        return count


class Puzzle:
    def __init__(self, lines):
        self.rules = {}

        for line in lines:
            new_line = line.replace("/", "")

            split = new_line.split(" => ")
            input = split[0]
            output = split[1]
            pre = np.array([c for c in input])
            post = np.array([c for c in output])
            if len(pre) == 4:
                pre_grid = pre.reshape((2, 2))
            else:
                pre_grid = pre.reshape((3, 3))

            for i in [0, 1, 2, 3]:
                rotated = np.rot90(pre_grid, i)
                key = "".join(c for c in rotated.flatten())
                self.rules[key] = post
                key = "".join(c for c in np.fliplr(rotated).flatten())
                self.rules[key] = post
                key = "".join(c for c in np.flipud(rotated).flatten())
                self.rules[key] = post

    def expand(self, grid):
        next = Grid(grid.next_size)
        for id, tile in grid.get_tile_iter():
            out = self.rules[tile]
            next.set_tile(id, out)
        return next

    def make_art(self, rounds):
        current = Grid(3)
        current.set_start()
        # current.print()
        for i in range(rounds):
            current = self.expand(current)
            # current.print()
        return current


def parse_input(lines):
    return Puzzle(lines)


def part1(puzzle):
    result = puzzle.make_art(5)
    return result.count_ons()


def part2(puzzle):
    result = puzzle.make_art(18)
    return result.count_ons()


# AB -> CA
# CD    BD
