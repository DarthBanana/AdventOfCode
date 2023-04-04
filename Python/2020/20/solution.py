## advent of code 2020
## https://adventofcode.com/2020
## day 20

import math
from aocpuzzle import *
import numpy as np
from PrettyMap2D import *
TOP_EDGE = 0
RIGHT_EDGE = 1
BOTTOM_EDGE = 2
LEFT_EDGE = 3
TOP_EDGE_FLIP = 4
RIGHT_EDGE_FLIP = 5
BOTTOM_EDGE_FLIP = 6
LEFT_EDGE_FLIP = 7

SIDES = [TOP_EDGE, RIGHT_EDGE, BOTTOM_EDGE, LEFT_EDGE]
ALL_ORIENTATIONS = SIDES + [TOP_EDGE_FLIP, RIGHT_EDGE_FLIP, BOTTOM_EDGE_FLIP, LEFT_EDGE_FLIP]

SEA_MONSTER1 = [Coord2D(0,0), Coord2D(1, 1), Coord2D(4,1), Coord2D(5,0), Coord2D(6,0), Coord2D(7,1), Coord2D(10,1), Coord2D(11,0), Coord2D(12,0), Coord2D(13,1), Coord2D(16,1), Coord2D(17,0), Coord2D(18,0), Coord2D(18, -1), Coord2D(19,0)]
SEA_MONSTER2 = [Coord2D(0,0), Coord2D(1, -1), Coord2D(4,-1), Coord2D(5,0), Coord2D(6,0), Coord2D(7,-1), Coord2D(10,-1), Coord2D(11,0), Coord2D(12,0), Coord2D(13,-1), Coord2D(16,-1), Coord2D(17,0), Coord2D(18,0), Coord2D(18, 1), Coord2D(19,0)]
SEA_MONSTER3 = [x.rotate_around_point(Coord2D(0,0), 90) for x in SEA_MONSTER1]
SEA_MONSTER4 = [x.rotate_around_point(Coord2D(0,0), 90) for x in SEA_MONSTER2]
SEA_MONSTER5 = [x.rotate_around_point(Coord2D(0,0), 180) for x in SEA_MONSTER1]
SEA_MONSTER6 = [x.rotate_around_point(Coord2D(0,0), 180) for x in SEA_MONSTER2]
SEA_MONSTER7 = [x.rotate_around_point(Coord2D(0,0), 270) for x in SEA_MONSTER1]
SEA_MONSTER8 = [x.rotate_around_point(Coord2D(0,0), 270) for x in SEA_MONSTER2]
SEA_MONSTERS = [SEA_MONSTER1, SEA_MONSTER2, SEA_MONSTER3, SEA_MONSTER4, SEA_MONSTER5, SEA_MONSTER6, SEA_MONSTER7, SEA_MONSTER8]

def get_flipped(side):
    return side + 4 if side < 4 else side - 4

class SubTile:
    def __init__(self, data):
        self.data = data.copy()
        self.edges = [self.data[0], self.data[:, 9], self.data[9], self.data[:, 0]]
        self.candidate_edges = [[],[],[],[]]

    def will_fit(self, top, left):
        if top is not None:
            if not np.array_equal(self.edges[TOP_EDGE], top):
                return False
        if left is not None:
            if not np.array_equal(self.edges[LEFT_EDGE], left):
                return False
        return True
    
    def is_edge(self, side):
        return len(self.candidate_edges[side]) == 0
    
    def is_same(self, side, data):
        if data is None:
            return self.is_edge(side)
        return np.array_equal(self.edges[side], data)
    
    def remove_edge(self, other_id, edge):
        reduced = False

        for side in SIDES:
            if (other_id, edge) in self.candidate_edges[side]:
                reduced = True
                self.candidate_edges[side].remove((other_id, edge))
            if (other_id, get_flipped(edge)) in self.candidate_edges[side]:
                reduced = True
                self.candidate_edges[side].remove((other_id, get_flipped(edge)))
        return reduced
    
    def __str__(self):
        string = '\nSubTile:\n'
        for i in range(10):
            for j in range(10):
                string += '#' if self.data[i, j] == 1 else '.'
            string += '\n'
        return string
    def __repr__(self):
        return self.__str__()
        
class Tile:
    def rotations(self):
        for r in range(4):
            a = np.rot90(self.original_data, r)
            yield (str(r) + "none", a)
            yield (str(r) + "fliplr", np.fliplr(a))
            #yield (str(r) + "flipud", np.flipud(a))            
            #yield (str(r) + "flipboth", np.flipud(np.fliplr(a)))
            
    def __init__(self, lines):        
        
        self.id = int(lines[0][5:-1])        

        self.original_data = np.zeros((10, 10), dtype=int)
        for i in range(10):
            self.original_data[i] = [1 if c == '#' else 0 for c in lines[i+1]]
        

        self.edges = [self.original_data[0], self.original_data[:, 9], self.original_data[9], self.original_data[:, 0]]
        self.edges += [np.flip(e) for e in self.edges]
        self.subtiles = []
        i = 0
        for rot in self.rotations():     
            st = SubTile(rot[1])
            self.subtiles.append(st)
            #if (i == 2 or i == 9):            
            i += 1


        self.candidate_edges = [[],[],[],[]]
        self.selected_subtile = None
                
    
    def set_subtile(self, i):
        self.selected_subtile = i
        
    def does_have_matching_edge(self, edge):
        for orientation in ALL_ORIENTATIONS:
            if np.array_equal(self.all_orientations[orientation], edge):
                return True
        return False
    
    def get_shared_edges(self, other):   
        for side in SIDES:
            for orientation in ALL_ORIENTATIONS:                
                if np.array_equal(self.edges[side], other.edges[orientation]):
                    self.candidate_edges[side].append((other.id, orientation % 4))                
                
    def build_sub_shared_edges(self):
        for side in SIDES:
            if len(self.candidate_edges[side]) == 0:
                continue

            for sub in self.subtiles:
                for sub_side in SIDES:
                    if sub.is_same(sub_side, self.edges[side]):
                        sub.candidate_edges[sub_side] = self.candidate_edges[side].copy()
                    elif sub.is_same(sub_side, np.flip(self.edges[side])):
                        sub.candidate_edges[sub_side] = self.candidate_edges[side].copy()
                


    def is_corner(self):   
        edge_count = 0
        for i in range(4):
            if len(self.candidate_edges[i]) > 0:
                edge_count += 1        
        return edge_count == 2
       
    def get_top_left(self):
        options = []
        for i in range(len(self.subtiles)):
            sub = self.subtiles[i]
            if sub.is_edge(TOP_EDGE) and sub.is_edge(LEFT_EDGE):
                options.append(i)
        return options
          
    def __str__(self):        
        string = '\nTile ' + str(self.id) + ':\n'
        data = self.original_data
        if self.selected_subtile is not None:
            string += str(self.selected_subtile) + '\n'
            data = self.subtiles[self.selected_subtile].data
        for i in range(10):
            for j in range(10):
                string += '#' if data[i, j] == 1 else '.'
            string += '\n'
        return string
    
    def __repr__(self):
        return self.__str__()
        
    def __getitem__(self, key):
        if self.selected_subtile is None:
            return self.original_data[key]
        return self.subtiles[self.selected_subtile].data[key]
    
    def remove_edge(self, other_id, edge):
        reduced = False
        if (other_id == self.id):
            return
        for side in SIDES:
            if (other_id, edge) in self.candidate_edges[side]:
                reduced = True
                self.candidate_edges[side].remove((other_id, edge))
            if (other_id, get_flipped(edge)) in self.candidate_edges[side]:
                reduced = True
                self.candidate_edges[side].remove((other_id, get_flipped(edge)))
        for sub in self.subtiles:
            reduced = sub.remove_edge(other_id, edge) or reduced
        return reduced
    
    def get_active_edge(self, side):
        sub = self.subtiles[self.selected_subtile]
        return sub.edges[side]
    
    def get_active_edge_candidates(self, side):
        sub = self.subtiles[self.selected_subtile]        
        if len(sub.candidate_edges[side]) == 1:
            return sub.candidate_edges[side]
        return None
    
    def get_candidate_subs(self, top_edge, left_edge):
        candidates = []
        for i in range(len(self.subtiles)):
            sub = self.subtiles[i]
            if sub.is_same(TOP_EDGE, top_edge) and sub.is_same(LEFT_EDGE, left_edge):
                candidates.append(i)
        return candidates


class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.always_run_part_1 = True
        self.tiles = []
        self.tile_table = {}
        num_tiles = len(lines) // 12
        print(num_tiles)
        for i in range(num_tiles):
            new_tile = Tile(lines[i*12:(i+1)*12])
            self.tiles.append(new_tile)
            self.tile_table[new_tile.id] = new_tile

        print(self.tiles)
        area = len(self.tiles)
        
        width = int(math.sqrt(area))
        height = int(math.sqrt(area))
        print('area: ' + str(area) + ' width: ' + str(width) + ' height: ' + str(height))
        assert (width * height == area)
        self.max_x = width - 1
        self.max_y = height - 1        
        self.map = {}
        self.grid = None
        
        #self.organize_all_candidates()        
        
        #self.grid = self.build_grid()        

    def reduce_candidates(self):
        reduced = False
        for t in self.tiles:
            for side in SIDES:
                if len(t.candidate_edges[side]) == 1:
                    consumed_edge = t.candidate_edges[side][0]
                    for other in self.tiles:
                        if other.id != t.id:
                            reduced = reduced or other.remove_edge(consumed_edge[0], consumed_edge[1])

        return reduced

    def get_all_candidates(self):
        for i in range(len(self.tiles)):            
            for j in range(len(self.tiles)):
                if i != j:
                    self.tiles[i].get_shared_edges(self.tiles[j])   

    def get_a_corner(self):
        for t in self.tiles:
            if t.is_corner():
                return t
            
    def reduce_all_candidates(self):
        while self.reduce_candidates():
            pass

    def build_grid(self):        

        grid = Map2D(default=".")
        x = 0
        y = 0
        keys = list(self.map.keys())
        keys.sort()
        print(keys)
        for by in range(self.max_y+1):
            for ty in range(1, 9):
                x = 0
                for bx in range(self.max_x+1):                    
                    tile = self.tile_table[self.map[Coord2D(bx, by)][0]]
                    for tx in range(1,9):
                        if tile[ty, tx] == 1:
                            grid[Coord2D(x,y)] = '#'
                        x += 1
                y += 1
        return grid

    
    def dfs2(self, coord, available):
        if coord.x > self.max_x:
            coord = Coord2D(0, coord.y + 1)
        if coord.y > self.max_y:
            return True
        candidates = available
        re = None
        be = None
        if coord.x > 0:
            left = self.map[coord + LEFT]
            lt = self.tile_table[left[0]]
            re = lt.get_active_edge(RIGHT_EDGE)
            c = lt.get_active_edge_candidates(RIGHT_EDGE)
            if c is None:
                return False
            if len(c) == 0:
                return False
            c = set([x[0] for x in c])
            candidates = candidates.intersection(c)
        if coord.y > 0:
            above = self.map[coord + UP]
            ut = self.tile_table[above[0]]
            be = ut.get_active_edge(BOTTOM_EDGE)
            c = ut.get_active_edge_candidates(BOTTOM_EDGE)
            if c is None:
                return False
            if len(c) == 0:
                return False
            c = set([x[0] for x in c])
            candidates = candidates.intersection(c)

        for t in candidates:
            next_tile = self.tile_table[t]
            subtiles = next_tile.get_candidate_subs(be, re)
            for s in subtiles:
                sub = next_tile.subtiles[s]
                if coord.x > 0:
                    left = self.map[coord + LEFT]
                    lt = self.tile_table[left[0]]
                    re = lt.get_active_edge(RIGHT_EDGE)
                    if not sub.is_same(LEFT_EDGE, re):
                        continue
                if coord.x == 0:
                    if not sub.is_edge(LEFT_EDGE):
                        continue
                if coord.y == 0:
                    if not sub.is_edge(TOP_EDGE):
                        continue
                if coord.x == self.max_x:
                    if not sub.is_edge(RIGHT_EDGE):
                        continue
                if coord.y == self.max_y:
                    if not sub.is_edge(BOTTOM_EDGE):
                        continue

                if coord.y > 0:
                    above = self.map[coord + UP]
                    ut = self.tile_table[above[0]]
                    be = ut.get_active_edge(BOTTOM_EDGE)
                    if not sub.is_same(TOP_EDGE, be):
                        continue
                

                next_tile.set_subtile(s)
                self.map[coord] = (next_tile.id, next_tile.selected_subtile)
                if self.dfs2(coord + RIGHT, available - set([t])):
                    return True
                del self.map[coord]  
    
    def propagate_candidates(self):
        for tile in self.tiles:
            tile.build_sub_shared_edges()

    def arrange_tiles(self):
        self.propagate_candidates()
        available = [t.id for t in self.tiles]
        # pick a corner:    
        coord = Coord2D(0,0)    
        tile = self.get_a_corner()
        tls = tile.get_top_left()
        tile.set_subtile(tls[0])
        self.map[coord] = (tile.id, tile.selected_subtile)                
        
        res = self.dfs2(Coord2D(0,0) + RIGHT, set(available))                 
        assert(res == True)

    def part1(self):
        self.get_all_candidates()
        self.reduce_all_candidates()
        self.arrange_tiles()
    
        self.grid = self.build_grid()
        self.grid.print()
        total = 1
        total *= self.map[Coord2D(0, 0)][0]
        total *= self.map[Coord2D(self.max_x, 0)][0]
        total *= self.map[Coord2D(0, self.max_y)][0]
        total *= self.map[Coord2D(self.max_x, self.max_y)][0]
        return total

    def is_this_monster(self, coord, monster):
        for m in monster:
            if self.grid[coord + m] != '#':
                return False
        return True
    
    def part2(self):
        
        for coord in self.grid:
            for monster in SEA_MONSTERS:
                if self.is_this_monster(coord, monster):
                    for m in monster:
                        self.grid[coord + m] = 'O'
        
        return self.grid.count('#')