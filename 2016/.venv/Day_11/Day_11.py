
from collections import Counter, deque, namedtuple
from itertools import chain, combinations
import re

State = namedtuple('State', ['floors', 'current_floor', 'steps', 'moves'])


def get_possible_moves(floor_contents):
    return chain(combinations(floor_contents, 2), combinations(floor_contents, 1))


def is_empty(floor_contents):
    return len(floor_contents) == 0


def is_safe(floor_contents):
    if len(set(type for _, type in floor_contents)) < 2:
        return True

    for (obj, type) in floor_contents:
        if type == 'microchip':
            if (obj, 'generator') not in floor_contents:
                return False
    return True


def parse_floors(inputstring):
    floors = []
    for line in inputstring.splitlines():
        floors.append(
            set(re.findall(r'(\w+)(?:-compatible)? (microchip|generator)', line)))
    return floors


def is_state_safe(floors):
    for floor in floors:
        if not is_safe(floor):
            return False
    return True


def is_state_final(floors):
    for i in range(0, len(floors) - 1):
        if not is_empty(floors[i]):
            return False
    return True


def print_state(state):

    for i in range(len(state.floors)):
        print()
        print(i, end=" ")
        if i == (state.current_floor):
            print('E', end=" ")
        else:
            print('.', end=" ")

        for item in state.floors[i]:
            if item[1] == "generator":
                print(item[0], end="G ")
            else:
                print(item[0], end="M ")

    print()


def get_state_signature(state):

    return (state.current_floor, tuple(tuple(Counter(type for _, type in floor).most_common()) for floor in state.floors))


def next_states(state):

    # print_state(floors)
    if not is_state_safe(state.floors):
        print("not safe")
        return

    if is_state_final(state.floors):
        print("final unexpectedly found")
        print(state.steps)
        return

    floor = state.floors[state.current_floor]
    possible_moves = get_possible_moves(floor)
    # print(moves)
    for move in possible_moves:
        for direction in [1, -1]:
            next_floor = state.current_floor + direction
            if not 0 <= next_floor < len(state.floors):
                continue

            next_floors = state.floors.copy()
            next_floors[state.current_floor] = next_floors[state.current_floor].difference(
                move)
            if not is_safe(next_floors[state.current_floor]):
                continue
            next_floors[next_floor] = next_floors[next_floor].union(move)
            if not is_safe(next_floors[next_floor]):
                continue
            new_moves = state.moves.copy()
            new_moves.append((move, direction))
            new_state = State(next_floors, next_floor,
                              state.steps + 1, new_moves)
            yield new_state


def solve(start_string):
    history = set()
    floors = parse_floors(start_string)
    starting_state = State(floors, 0, 0, deque())
    queue = deque([starting_state])

    while queue:
        state = queue.popleft()
        next_floors, floor, steps, moves = state
        if is_state_final(state.floors):

            return State(floors, 0, state.steps, state.moves)

        for next_state in next_states(state):
            if (signature := get_state_signature(next_state)) not in history:
                history.add(signature)
                queue.append(next_state)


def replay_moves(state):

    print_state(state)

    moves = state.moves
    move, direction = moves.popleft()
    print(move)

    next_floor = state.current_floor + direction
    assert (0 <= next_floor < len(state.floors))
    next_floors = state.floors.copy()
    next_floors[state.current_floor] = next_floors[state.current_floor].difference(
        move)
    assert (is_safe(next_floors[state.current_floor]))

    next_floors[next_floor] = next_floors[next_floor].union(move)
    assert (is_safe(next_floors[next_floor]))
    next_state = State(next_floors, next_floor, state.steps - 1, moves)
    if (len(moves) > 0):
        replay_moves(next_state)


test_start = """\
The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant."""

real_start = """\
The first floor contains a thulium generator, a thulium-compatible microchip, a plutonium generator, and a strontium generator.
The second floor contains a plutonium-compatible microchip and a strontium-compatible microchip.
The third floor contains a promethium generator, a promethium-compatible microchip, a ruthenium generator, and a ruthenium-compatible microchip.
The fourth floor contains nothing relevant."""
real_start_2 = """\
The first floor contains a thulium generator, a thulium-compatible microchip, a plutonium generator, a strontium generator, a elerium generator, a elerium-compatible microchip, a dilithium generator, and a dilithium-compatible microchip.
The second floor contains a plutonium-compatible microchip and a strontium-compatible microchip.
The third floor contains a promethium generator, a promethium-compatible microchip, a ruthenium generator, and a ruthenium-compatible microchip.
The fourth floor contains nothing relevant."""

result = solve(test_start)
print(result.steps)
assert (result.steps == 11)
replay_moves(result)

result = solve(real_start)
print(result.steps)

result = solve(real_start_2)
print(result.steps)
