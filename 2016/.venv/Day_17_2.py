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

def find_longest_path(password):
    longest_path = ""
    visited = set()
    queue = deque([(password, (0,0))])

    while queue:
        pass_string, location = queue.popleft()

        if location == TARGET:
            if len(pass_string) > len(longest_path):
                longest_path = pass_string    
            continue                

        for next in get_next_steps(pass_string, location):
            next_location = next[1]
            if next_location in visited:
                continue
            queue.append(next)

    return len(longest_path) - len(password)
        

def test(password, expected):
    result = find_longest_path(password)
    print(result)
    assert(result == expected)

test("ihgpwlah", 370)
test("kglvqrro", 492)
test("ulqzkmiv", 830)

print("Part 2 result : ", find_longest_path(REAL_INPUT))
