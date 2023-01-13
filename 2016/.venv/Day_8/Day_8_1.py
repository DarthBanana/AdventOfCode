import os
import re


def open_file(file):
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    absolute_path = absolute_path + '\\'
    file_path = absolute_path + file
    input_file = open(file_path, "r")
    return input_file


class Display:
    def __init__(self, width, height):
        self.pixels = [[False for i in range(width)] for i in range(height)]
        self.width = width
        self.height = height

    def rect(self, width, height):
        assert (width <= self.width)
        assert (height <= self.width)

        for y in range(height):
            for x in range(width):
                self.pixels[y][x] = True

    def reset(self):
        self.pixels = [[False]*self.width]*self.height

    def rotate_row(self, row, amount):
        new_row = [False for i in range(self.width)]
        for i in range(self.width):
            new_i = (i + amount) % self.width
            new_row[new_i] = self.pixels[row][i]
        for i in range(self.width):
            self.pixels[row][i] = new_row[i]

    def rotate_column(self, column, amount):
        new_col = [False for i in range(self.height)]
        for i in range(self.height):
            new_i = (i + amount) % self.height
            new_col[new_i] = self.pixels[i][column]

        for i in range(self.height):
            self.pixels[i][column] = new_col[i]

    def execute_instruction(self, instruction_string):
        rect_re = re.compile(r"rect (\d+)x(\d+)")
        rot_row = re.compile(r"rotate row y=(\d+) by (\d+)")
        rot_col = re.compile(r"rotate column x=(\d+) by (\d+)")

        match = rect_re.search(instruction_string)
        if (match):
            self.rect(int(match.group(1)), int(match.group(2)))
            return

        match = rot_row.search(instruction_string)
        if (match):
            self.rotate_row(int(match.group(1)), int(match.group(2)))
            return

        match = rot_col.search(instruction_string)
        if (match):
            self.rotate_column(int(match.group(1)), int(match.group(2)))
            return
        assert (False)

    def execute_program(self, filename):
        file = open_file(filename)
        for line in file.readlines():
            self.execute_instruction(line)

    def count_on_lights(self):
        count = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.pixels[y][x]:
                    count += 1
        return count

    def draw(self):
        print()
        for y in range(self.height):
            for x in range(self.width):
                if self.pixels[y][x]:
                    print('#', end="")
                else:
                    print('.', end="")
            print()


def test():
    rot_col = re.compile(r"rotate column x=(\d+) by (\d+)")
    assert (rot_col.search("rotate column x=1 by 1"))
    display = Display(7, 3)
    display.draw()
    display.execute_instruction("rect 3x2")
    display.draw()

    assert display.count_on_lights() == 6

    display.execute_instruction("rotate column x=1 by 1")
    display.draw()

    display.execute_instruction("rotate row y=0 by 4")
    display.draw()

    display.execute_instruction("rotate column x=1 by 1")
    display.draw()


def run():
    display = Display(50, 6)
    display.execute_program("input.txt")
    display.draw()
    return display.count_on_lights()


print(run())
