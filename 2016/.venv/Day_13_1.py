from collections import deque
import gmpy2
magic_number = 10
directions = [(0,-1), (1,0), (0,1), (-1,0)]

def is_location_wall(location):
    x, y = location
    value = x*x + 3*x + 2*x*y + y + y*y
    value += magic_number

    num_bits = gmpy2.bit_count(value)
    if num_bits & 0x1:
        return True

    return False

def get_next_locations(location):
    x, y = location
    next_locations = []
    for (dx, dy) in directions:
        new_x = x + dx
        new_y = y + dy
        if x == 0 or y == 0:
            continue
        new_location = (new_x, new_y)
        if is_location_wall(new_location):
            continue
        next_locations.append(new_location)
    return next_locations

def find_shortest_path(target):
    history = set()

    queue = deque([((1,1), 0)])
    while queue:
        location, steps = queue.popleft()

        if location == target:
            return steps

        for next_location in get_next_locations(location):
            if next_location not in history:
                queue.append((next_location, steps + 1))
                history.add(next_location)




magic_number = 10
assert(find_shortest_path((7,4)) == 11)
magic_number = 1362
print(find_shortest_path((31,39)))


    


