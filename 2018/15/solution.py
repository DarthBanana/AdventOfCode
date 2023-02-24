## advent of code 2018
## https://adventofcode.com/2018
## day 15

from collections import deque
import copy
from Map2DLayers import *
class Unit:
    def __init__(self, goblin, coord):
        self.goblin = goblin
        self.coord = coord
        self.attack_power = 3
        self.hit_points = 200
        self.alive = True

class Puzzle:
    def __init__(self, lines):
        self.map = InfiniteGridStack(default=".")
        self.player_map = {}
        self.map.add_layer(self.player_map)
        self.original_units = []
        self.valid_coords = set()        
        y = 0
        for line in lines:
            x = 0
            for c in line:
                coord = Coord2D(x,y)
                if c == "#":
                    self.map[coord] = "#"
                elif c == "G":        
                    self.valid_coords.add(coord)     
                    self.original_units.append(Unit(True, coord))                    
                elif c == "E":
                    self.valid_coords.add(coord)
                    self.original_units.append(Unit(False, coord))                    
                elif c == ".":
                    self.valid_coords.add(coord)                           
                elif c == " ":
                    break
                x += 1
            y += 1             
                        
        self.reset()

    def reset(self, elf_attack_power=3):
        self.elf_died = False
        self.active_units = copy.deepcopy(self.original_units)
        self.player_map.clear()
        
        for unit in self.active_units:
            if unit.goblin:
                self.player_map[unit.coord] = "G"
            else:
                unit.attack_power = elf_attack_power
                self.player_map[unit.coord] = "E"        

    def get_next_move(self, coordA, coords):

        visited = {}
        queue = deque()
        queue.append((coordA, 0, []))
        found = []
        found_dist = 1000000000        
        while queue:            
            coord, dist, steps = queue.popleft()            
            assert(dist < 100)
            if dist > found_dist:                
                break

            if coord in visited:
                # only filter on those coords that were
                # visited in fewer steps.  We want to get the list
                # of all candidate paths to all candidate locations with 
                # the minimum number of steps
                vdist, vstep = visited[coord]
                if dist > vdist:
                    continue
                if not (steps[0] < vstep):                    
                    continue
                            
            if dist > 0:    
                visited[coord] = (dist, steps[0])
            else:
                visited[coord] = (dist, Coord2D(0,0))
            
            if coord in coords:
                found_dist = dist
                found.append((coord, steps))
                continue
            for n in coord.neighbor_coords():
                if self.map[n] == ".":

                    next_steps = steps.copy()
                    next_steps.append(n)
                    queue.append((n, dist + 1, next_steps))
            
        if len(found) == 0:            
            return coordA

        # We have all of the paths to any of the target coords that have the
        # same shortest path length  Now sort them based on the reading order
        # of the destination, then the reading order of the first step
        found.sort(key=lambda x: (x[0], x[1][0]))
        
        dest, steps = found[0]
        
        return steps[0]
    
    def move(self, unit, targets):        
        candidate_squares = set()        
        for target in targets:
            for loc in target.coord.neighbor_coords():
                if self.map[loc] == ".":
                    candidate_squares.add(loc)

        new_location = self.get_next_move(unit.coord, candidate_squares)
        self.player_map.pop(unit.coord)
        
        if unit.goblin:
            self.player_map[new_location] = "G"
        else:
            self.player_map[new_location] = "E"
        unit.coord = new_location
 
    def in_range(self, unit, targets):
        neighbors = set(unit.coord.neighbor_coords())
        potential_victims = []
        for t in targets:
            if t.coord in neighbors:
                if t.hit_points > 0:
                    potential_victims.append(t)
        return potential_victims

    def attack(self, unit, potential_victims):        
        if len(potential_victims) == 0:
            return        

        potential_victims.sort(key=lambda x:(x.hit_points, x.coord))
        victim = potential_victims[0]
        victim.hit_points -= unit.attack_power
        
        if victim.hit_points <= 0:
            if not victim.goblin:
                self.elf_died = True
            self.player_map.pop(victim.coord)
        



    def execute_turn(self, unit):     
        targets = [x for x in self.active_units if (not x.goblin == unit.goblin) and (x.hit_points > 0)] #filter(lambda x:not x.goblin == unit.goblin, self.active_units))        
        if (len(targets)) == 0:           
            return False

        in_range = self.in_range(unit, targets)
        if len(in_range) == 0:
            self.move(unit, targets)
            in_range = self.in_range(unit, targets)
        self.attack(unit, in_range)
        return True

    def remove_the_dead(self):
        new_active_units = []
        for u in self.active_units:
            if u.hit_points > 0:
                new_active_units.append(u)
        self.active_units = new_active_units

    def execute_round(self):
        
        self.active_units.sort(key=lambda x: x.coord)        
        for unit in self.active_units:  
            if unit.hit_points > 0:          
                if not self.execute_turn(unit):
                    self.remove_the_dead()
                    return False
        self.remove_the_dead()
        return True

    def play_game(self):
        round = 0
        while(self.execute_round()):
            round += 1           

        total_hp = 0
        for unit in self.active_units:
            total_hp += unit.hit_points
        outcome = total_hp * round
        return outcome

    def try_with_ap(self, ap):
        print("Trying attack power:", ap)
        self.reset(ap)
        
        round = 0
        while(self.execute_round()):
            round += 1

            if self.elf_died:
                print("Elf died")
                return 0    

        if self.elf_died:
                print("Elf died2")
                return 0    
        total_hp = 0
        for unit in self.active_units:
            total_hp += unit.hit_points
        outcome = total_hp * round
        return outcome

    def save_the_elves(self):        
        ap = 3
        while True:
            
            outcome = self.try_with_ap(ap)
            print(outcome)
            if outcome > 0:
                return outcome
            ap += 1

    def part1(self):
        return self.play_game()
        

    def part2(self):
        return self.save_the_elves()
