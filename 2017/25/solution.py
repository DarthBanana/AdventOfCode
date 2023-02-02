# advent of code 2017
# https://adventofcode.com/2017
# day 25

import re


class Action:
    def __init__(self, write, move, next):
        self.write = write
        if move == "right":
            self.move = 1
        elif move == "left":
            self.move = -1
        else:
            assert False
        self.next = next


class State:
    def __init__(
        self,
        id,
        write_on_zero,
        move_on_zero,
        next_on_zero,
        write_on_one,
        move_on_one,
        next_on_one,
    ):
        self.id = id
        self.actions = []
        self.actions.append(Action(write_on_zero, move_on_zero, next_on_zero))
        self.actions.append(Action(write_on_one, move_on_one, next_on_one))


begin_re = re.compile(r"Begin in state (\w)")
steps_re = re.compile(r"Perform a diagnostic checksum after (\d+) steps.")
state_re = re.compile(
    r"In state (\w):\s*If the current value is 0:\s*- Write the value (\d).\s*- Move one slot to the (\w+).\s*- Continue with state (\w).\s*If the current value is 1:\s*- Write the value (\d).\s*- Move one slot to the (\w+).\s*- Continue with state (\w)."
)


class Puzzle:
    def __init__(self, lines):

        text = "".join(lines)
        match = begin_re.search(text)
        self.start_state = match.group(1)
        self.states = {}
        match = steps_re.search(text)
        self.steps = int(match.group(1))

        for match in state_re.finditer(text):
            state = State(
                match.group(1),
                int(match.group(2)),
                match.group(3),
                match.group(4),
                int(match.group(5)),
                match.group(6),
                match.group(7),
            )
            self.states[state.id] = state
        self.reset()

    def reset(self):
        self.position = 0
        self.tape = set()
        self.state = self.start_state

    def step(self):
        state = self.states[self.state]
        if self.position in self.tape:
            value = 1
        else:
            value = 0

        action = state.actions[value]
        if action.write == 1:
            self.tape.add(self.position)
        elif value == 1:
            self.tape.remove(self.position)
        self.position += action.move
        self.state = action.next

    def run(self):
        for i in range(self.steps):
            self.step()
        return len(self.tape)


def parse_input(lines):
    return Puzzle(lines)


def part1(puzzle):
    return puzzle.run()


def part2(puzzle):
    pass
