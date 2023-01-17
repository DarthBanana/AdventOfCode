from collections import deque
import hashlib
import re
DIRECTIONS = [((0,-1), 'U', 0), ((1,0), 'R', 3), ((0,1), 'D', 1), ((-1,0), 'L', 2)]
TARGET = (3,3)
REAL_INPUT = "pgflpeqp"

def get_next_steps(pass_string, location):
    next_steps = []
    x, y = location
    hash = hashlib.md5(pass_string.encode("utf-8"))
    hash = hash.hexdigest()
    for direction in DIRECTIONS:
        new_x = x + direction[0][0]
        new_y = y + direction[0][1]
        if not 0 <= new_x < 4:
            continue
        if not 0 <= new_y < 4:
            continue
        door = hash[direction[2]]
        if door.isdigit() or door == 'a':
            #door is locked
            continue

        next_steps.append((pass_string + direction[1], (new_x, new_y)))

    return next_steps

def find_shortest_path(password):
    visited = set()
    queue = deque([(password, (0,0))])

    while queue:
        pass_string, location = queue.popleft()

        if location == TARGET:
            return pass_string[len(password):]
        #visited.add(location)

        for next in get_next_steps(pass_string, location):
            next_location = next[1]
            if next_location in visited:
                continue
            queue.append(next)
        

def test(password, expected):
    result = find_shortest_path(password)
    print(result)
    assert(result == expected)

test("ihgpwlah", "DDRRRD")
test("kglvqrro", "DDUDRLRRUDRD")
test("ulqzkmiv", "DRURDRUDDLLDLUURRDULRLDUUDDDRR")

print("Part 1 result : ", find_shortest_path(REAL_INPUT))
