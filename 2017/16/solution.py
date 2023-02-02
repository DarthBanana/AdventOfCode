## advent of code 2017
## https://adventofcode.com/2017
## day 16

from collections import deque
import re

spin_re = re.compile(r"s(\d+)")
exchange_re = re.compile(r"x(\d+)/(\d+)")
partner_re = re.compile(r"p(\w+)/(\w+)")


class Puzzle:
    def __init__(self, lines):
        if len(lines[0]) > 20:
            self.dancer_count = 16
            self.dancers = deque(
                [
                    "a",
                    "b",
                    "c",
                    "d",
                    "e",
                    "f",
                    "g",
                    "h",
                    "i",
                    "j",
                    "k",
                    "l",
                    "m",
                    "n",
                    "o",
                    "p",
                ]
            )
        else:
            self.dancer_count = 5
            self.dancers = deque(["a", "b", "c", "d", "e"])

        print(self.dancers)
        self.instructions = []
        for command in lines[0].split(","):
            if match := spin_re.search(command):
                self.instructions.append(("s", int(match.group(1))))
            elif match := exchange_re.search(command):
                self.instructions.append(
                    ("x", (int(match.group(1)), int(match.group(2))))
                )
            elif match := partner_re.search(command):
                self.instructions.append(("p", (match.group(1), match.group(2))))
            else:
                assert False

    def reset_dancers(self):
        if self.dancer_count == 16:
            self.dancers = deque(
                [
                    "a",
                    "b",
                    "c",
                    "d",
                    "e",
                    "f",
                    "g",
                    "h",
                    "i",
                    "j",
                    "k",
                    "l",
                    "m",
                    "n",
                    "o",
                    "p",
                ]
            )
        else:
            self.dancers = deque(["a", "b", "c", "d", "e"])

    def spin(self, distance):
        self.dancers.rotate(distance)

    def exchange(self, index1, index2):

        val = self.dancers[index1]
        self.dancers[index1] = self.dancers[index2]
        self.dancers[index2] = val

    def swap(self, a, b):
        index1 = self.dancers.index(a)
        index2 = self.dancers.index(b)
        self.exchange(index1, index2)

    def execute(self):
        for op, params in self.instructions:
            if op == "s":
                self.spin(params)
            elif op == "x":
                self.exchange(params[0], params[1])
            elif op == "p":
                self.swap(params[0], params[1])
            else:
                assert False


def parse_input(lines):
    puzzle = Puzzle(lines)
    return puzzle


def part1(puzzle):
    puzzle.execute()
    return "".join(puzzle.dancers)


def part2(puzzle):
    seen = {}
    # find the solution after one path
    iterations = 0
    puzzle.reset_dancers()
    result = ""
    not_found = True
    while iterations < 1000000000:
        iterations += 1
        puzzle.execute()

        if not_found:
            result = "".join(puzzle.dancers)
            if result in seen.keys():
                last_iteration = seen[result]
                iteration_length = iterations - last_iteration
                print(last_iteration, iterations)
                iterations_remaining = (1000000000 - last_iteration) % iteration_length
                iterations = 1000000000 - iterations_remaining
                print(iterations)
                not_found = False
            seen[result] = iterations

    return "".join(puzzle.dancers)
