from collections import deque
import gmpy2
magic_number = 1362
directions = [(0,-1), (1,0), (0,1), (-1,0)]

def is_location_wall(location):
    
    x, y = location

    if x < 0:
        return True
    if y < 0:
        return True

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
        new_location = (new_x, new_y)
        if is_location_wall(new_location):
            continue
        next_locations.append(new_location)
    return next_locations

def find_shortest_path(depth):
    history = set()
    
    queue = deque([((1,1), 0)])
    while queue:
        location, steps = queue.popleft()

        if steps > depth:
            continue            

        history.add(location)

        for next_location in get_next_locations(location):
            if not next_location in history:
                queue.append((next_location, steps + 1))                

    return len(history)


# higher than 135, and 136
print(find_shortest_path(50))


    


