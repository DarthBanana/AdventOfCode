import array
from collections import deque
import copy
import os
import re


def open_file(file):
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    absolute_path = absolute_path + '\\'
    file_path = absolute_path + file
    input_file = open(file_path, "r")
    return input_file


node_re = re.compile(
    r"/dev/grid/node-x(\d+)-y(\d+) \s*(\d+)T \s*(\d+)T \s*(\d+)T \s*(\d+)%")
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
map = {}


class Node:
    def __init__(self, string):
        self.name = string.split()[0]
        match = node_re.search(string)
        assert (match)
        self.x = int(match.groups()[0])
        self.y = int(match.groups()[1])
        self.size = int(match.groups()[2])
        self.used = int(match.groups()[3])
        self.avail = int(match.groups()[4])
        self.use = int(match.groups()[5])
        self.index = 100000000

#
#
#  So, looking at the data, there are a few very large nodes whose used data is greater than the capacity of most of the others.
#  For all the others, their used value is always less that the capacity of all of the others.
#  There is always 1 empty node, and not enough room in the other nodes to bother moving data to a non-empty node
#
#  So, I decided to just track the very large nodes as "bad nodes", and just not included them in any movement
#  Then I didn't need to track any of the sizes, only where the empty node was and the interesting data was
#  Every movement from a->b moved the empty node from b->a.  if a happened to be the location of the interesting
#  data, then interesting data moved from a->b
#


class Grid:
    sizes = None
    bad_locations = set()
    max_x = 0
    max_y = 0

    def __init__(self, nodes):
        sizes = None
        Grid.bad_locations.clear()
        self.steps = 0

        for node in nodes:

            if node.used == 0:
                self.empty = (node.x, node.y)
            Grid.max_x = max(self.max_x, node.x)
            Grid.max_y = max(self.max_y, node.y)
            if node.used > 80:
                Grid.bad_locations.add((node.x, node.y))

        self.data_location = (Grid.max_x, 0)

    def get_viable_pairs(self):
        b_location = self.empty
        a_options = []
        pairs = []
        for dx, dy in DIRECTIONS:
            new_x = b_location[0] + dx
            if not 0 <= new_x <= Grid.max_x:
                continue
            new_y = b_location[1] + dy
            if not 0 <= new_y <= Grid.max_y:
                continue
            if (new_x, new_y) in Grid.bad_locations:
                continue
            pairs.append(((new_x, new_y), self.empty))

        return pairs

    def move(self, pair):

        if pair[0] == self.data_location:
            self.data_location = pair[1]
        self.empty = pair[0]
        self.steps += 1

    def is_final(self):
        return self.data_location == (0, 0)

    def get_hash(self):
        return (self.empty, self.data_location)


def get_nodes(filename):
    file = open_file(filename)
    nodes = []
    for line in file.readlines():
        nodes.append(Node(line))

    return nodes


def get_shortest_path(grid):
    queue = deque([grid])
    last_step = 0
    seen = set()
    while queue:

        grid = queue.popleft()
        if grid.steps != last_step:
            print("steps: ", grid.steps, "queue : ", len(queue))
        last_step = grid.steps

        if grid.is_final():
            return grid.steps, grid

        pairs = grid.get_viable_pairs()
        if not pairs:
            continue
        for pair in pairs:
            next_grid = copy.deepcopy(grid)
            next_grid.move(pair)
            hash = next_grid.get_hash()
            if hash in seen:
                continue
            seen.add(hash)
            queue.append(next_grid)

    assert (False)


def solve(filename):
    nodes = get_nodes(filename)
    grid = Grid(nodes)

    result, last_grid = get_shortest_path(grid)
    return result, last_grid


result, history = solve("test.txt")
print(result)
print(history)

result, history = solve("input.txt")
print("Result for Part 2 : ", result)
