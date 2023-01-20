from collections import deque
import os

DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
PART_2 = False


def open_file(file):
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    absolute_path = absolute_path + '\\'
    file_path = absolute_path + file
    input_file = open(file_path, "r")
    return input_file


class Map:
    def __init__(self, filename):
        self.map = set()
        self.distances = {}
        self.pois = []
        file = open_file(filename)
        self.min_distance = 100000000000
        self.point_distances = {}

        y = 0
        for line in file.readlines():
            x = 0
            for c in line:
                if c == '.':
                    self.map.add((x, y))
                elif c == '0':
                    self.start = (x, y)
                    self.pois.append(((x, y), c))
                    self.map.add((x, y))

                elif c.isdigit():
                    self.pois.append(((x, y), c))
                    self.map.add((x, y))
                x += 1
            y += 1

        self.get_shortests_paths()

    def next_steps(self, position):
        x, y = position
        for dx, dy in DIRECTIONS:
            new_point = (x + dx, y + dy)
            if new_point in self.map:
                yield (new_point)

    def get_shortests_bfs(self, pos, poi):
        tbf = set()
        for poi2 in self.pois:
            if (pos, poi) in self.distances:
                continue
            tbf.add(poi2[0])

        seen = set()
        queue = deque([(pos, 0)])

        while queue and len(tbf):
            loc, steps = queue.popleft()

            for next in self.next_steps(loc):
                if next in seen:
                    continue
                seen.add(next)
                if next in tbf:
                    tbf.remove(next)
                    for p in self.pois:
                        if p[0] == next:
                            self.distances[(poi, p[1])] = steps + 1
                            self.distances[(p[1], poi)] = steps + 1
                queue.append((next, steps + 1))

    def get_shortests_paths(self):

        for poi in self.pois:
            self.get_shortests_bfs(poi[0], poi[1])

    def next_step(self, position, distance, unvisited):
        if len(unvisited) == 0:
            if PART_2:
                distance_to_start = self.distances[(position, '0')]
                distance += distance_to_start
            self.min_distance = min(self.min_distance, distance)
            return

        for next in unvisited:
            step_distance = self.distances[(position, next)]
            next_unvisited = unvisited.copy()
            next_unvisited.remove(next)
            self.next_step(next, distance + step_distance, next_unvisited)

    def reach_all_points(self):
        unvisited = []
        for pos, node in self.pois:
            if node == '0':
                continue
            unvisited.append(node)

        self.next_step('0', 0, unvisited)
        return self.min_distance


test_map = Map("test.txt")
result = test_map.reach_all_points()
print(result)
assert (result == 14)

real_map = Map("input.txt")
result = real_map.reach_all_points()
print("Result for part 1 : ", result)

real_map = Map("input.txt")
PART_2 = True
result = real_map.reach_all_points()
print("Result for part 1 : ", result)
