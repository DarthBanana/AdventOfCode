## advent of code 2017
## https://adventofcode.com/2017
## day 24


class Puzzle:
    def __init__(self, lines):
        self.components = set()
        for line in lines:
            split = line.split("/")
            a = int(split[0])
            b = int(split[1])
            self.components.add(frozenset([a, b]))
        self.highest_score = 0
        self.longest_bridge = 0
        self.longest_bridge_scores = []

    def next_step(self, so_far, next, score, available):
        self.highest_score = max(self.highest_score, score)
        if len(so_far) > self.longest_bridge:
            self.longest_bridge = len(so_far)
            self.longest_bridge_scores = [score]
        elif len(so_far) == self.longest_bridge:
            self.longest_bridge_scores.append(score)

        for c in available:
            if next in c:
                next_attach = next
                node_score = 0
                for v in c:
                    node_score += v
                    if v != next:
                        next_attach = v
                if len(c) == 1:
                    node_score *= 2
                next_available = available.copy()
                next_available.remove(c)
                next_so_far = so_far.copy()
                next_so_far.add(c)
                self.next_step(
                    next_so_far, next_attach, score + node_score, next_available
                )
                # what is the other number


def parse_input(lines):
    return Puzzle(lines)


def part1(puzzle):
    puzzle.next_step(set(), 0, 0, puzzle.components)
    return puzzle.highest_score


def part2(puzzle):
    puzzle.longest_bridge_scores.sort()
    puzzle.longest_bridge_scores.reverse()
    print(puzzle.longest_bridge)
    return puzzle.longest_bridge_scores[0]
