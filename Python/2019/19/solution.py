## advent of code 2019
## https://adventofcode.com/2019
## day 19

from time import sleep
from PrettyMap2D import *
from aocpuzzle import *
from intcode import *

BOX_SIZE = 100
class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.input_mailbox = Mailbox()
        self.output_mailbox = Mailbox()
        self.computer = MyIntcodeComputer(self.input_mailbox, self.output_mailbox)
        self.computer.load_program_from_input(lines)
        self.computer.reset()
        self.map = None
        

    def try_coord_no_map(self, coord):
        self.computer.reset()
        self.input_mailbox.send(coord.x)
        self.input_mailbox.send(coord.y)
        self.computer.run()
        
        assert(len(self.output_mailbox) == 1)
        res = self.output_mailbox.receive()
        return res

    def try_coord(self, coord):
        res = self.try_coord_no_map(coord)        
        if res == 1:
            self.map[coord] = "#"
        else:
            self.map[coord] = "."
        return res

    def test_row(self, first_x, last_x, y, max = 50):
        x = first_x
        found_start = False
        while(True):
            if x > first_x + 10:
                break
            coord = Coord2D(x, y)
            res = self.try_coord_no_map(coord)
            if res == 1:
                first_x = x
                found_start = True
                break
            x += 1
        if not found_start:
            return (first_x, last_x)

        if last_x < first_x:
            last_x = first_x

        x = last_x

        while(x < max):
            coord = Coord2D(x,y)
            res = self.try_coord_no_map(coord)
            if res == 0:
                break
            last_x = x
            x += 1
        return (first_x, last_x)

    def part1_fast(self):
        first_x = 0
        last_x = 0
        count = 0
        y = 0
        for y in range(50):
            #print(y, first_x, last_x)
            (first_x, last_x) = self.test_row(first_x, last_x, y)
            count = count + (last_x - first_x + 1)
        return count

    def part1(self):     
        return self.part1_fast()   

    def check_coord(self, coord):
        if self.try_coord_no_map(coord) == 0:
            return False
        if self.try_coord_no_map(coord + Coord2D(BOX_SIZE-1, 0)) == 0:
            return False
        if self.try_coord_no_map(coord + Coord2D(0, BOX_SIZE-1)) == 0:
            return False
        return True
    
    def find_part2_coord(self):
        first_x = 0
        last_x = 0        
        y = 0
        while(True):
            
            (first_x, last_x) = self.test_row(first_x, last_x, y, 10000)
            #print(y, first_x, last_x)
            width = (last_x - first_x) + 1
            if width >= BOX_SIZE:
                start_x = last_x - (BOX_SIZE-1)
                coord = Coord2D(start_x, y + (BOX_SIZE-1))
                res = self.try_coord_no_map(coord)
                if res == 1:
                    coord = Coord2D(start_x, y)
                    print("Found it!", coord)
                    
                    assert(self.check_coord(coord))

                    while (self.check_coord(coord + UP)):
                        
                        coord = coord + UP
                        print("Found another: ", coord)
                    return coord
            y += 1

    def part2(self):     
        coord = self.find_part2_coord()
        #assert(0 == self.try_coord_no_map(coord + BOX_SIZE*RIGHT))
        if (False):
            self.map = PrettyMap2D()

            self.map.autodraw = False
            self.map.clear()
            for y in range(coord.y-10, coord.y + BOX_SIZE+10):
                self.map.refresh()
                for x in range(coord.x-10, coord.x + BOX_SIZE+10):
                    new_coord = Coord2D(x,y)
                    #print(new_coord)
                    if x in range(coord.x, coord.x+BOX_SIZE) and y in range(coord.y, coord.y + BOX_SIZE):
                        self.map[new_coord] = " "
                    else:
                        self.try_coord(new_coord)
            while(True):
                self.map.refresh()
                sleep(0.1)
        result = 10000*coord.x + coord.y
        return result




    


        