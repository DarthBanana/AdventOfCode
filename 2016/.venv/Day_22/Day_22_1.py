import os
import re

def open_file(file):
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    absolute_path = absolute_path + '\\'
    file_path = absolute_path + file
    input_file = open(file_path, "r")
    return input_file

node_re = re.compile(r"/dev/grid/node-x(\d+)-y(\d+) \s*(\d+)T \s*(\d+)T \s*(\d+)T \s*(\d+)%")


class Node:
    def __init__(self, string):
        self.name = string.split()[0]
        match = node_re.search(string)
        assert(match)
        self.x = int(match.groups()[0])
        self.y = int(match.groups()[1])
        self.size = int(match.groups()[2])
        self.used = int(match.groups()[3])
        self.avail = int(match.groups()[4])
        self.use = int(match.groups()[5])

def get_nodes(filename):
    file = open_file(filename)
    nodes = []
    for line in file.readlines():
        nodes.append(Node(line))

    return nodes

def get_viable_pairs(nodes):
    pairs = []
    for a in nodes:        
        if a.used == 0:
            continue
        for b in nodes:
            if b == a:
                continue
            if a.used <= b.avail:
                pairs.append((a,b))
    for pair in pairs:
        print(pair[0].name, pair[1].name)
    return pairs

            

nodes = get_nodes("input.txt")
pairs = get_viable_pairs(nodes)
print("Part 1 result : ", len(pairs))


