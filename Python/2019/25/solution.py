## advent of code 2019
## https://adventofcode.com/2019
## day 25

from aocpuzzle import *
from intcode import *

INSTRUCTIONS1 = """\
east
take antenna
west
north
take weather machine
north
take klein bottle
east
take spool of cat6
east
south
take mug
north
north
west
north
take cake
south
east
east
north
north
take tambourine
south
south
south
take shell
north
west
south
west
south
south
"""

#Trying  {'mug', 'weather machine', 'antenna', 'spool of cat6'}
INSTRUCTIONS2 = """\
east
take antenna
west
north
take weather machine
north
east
take spool of cat6
east
south
take mug
north
west
south
south
east
"""

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.computer = MyIntcodeComputer()
        self.terminal = InteractiveAsciiComputer(self.computer)
        self.computer.load_program_from_input(lines)
        self.history = set()

    def drop_object(self, object):
        self.terminal.feed("drop " + object + "\n")
        self.computer.run()
        self.terminal.get_output()

    def pick_up_object(self, object):
        self.terminal.feed("take " + object + "\n")
        self.computer.run()
        self.terminal.get_output()

    def find_weight(self, objects_left, objects_holding):
        hash = frozenset(objects_left)
        if hash in self.history:
            return False
        self.history.add(hash)
        print("Trying ", objects_holding)        

        #self.terminal.feed("inv\n")
        #print(self.terminal.get_output())
        self.terminal.feed("east\n")
        
        self.computer.run()
        output = self.terminal.get_output()
        #print(output)
        if "lighter" in output:
            print("too heavy")
            return False
        elif "heavier" in output:
            print("too light")
            for o in objects_left:
                self.pick_up_object(o)
                if self.find_weight(objects_left - {o}, objects_holding | {o}):
                    return True
                self.drop_object(o)
        else:
            print(output)
            return True

        return False
    def part1(self):
        #Trying  {'mug', 'weather machine', 'antenna', 'spool of cat6'}
        #objects = {"antenna", "weather machine", "klein bottle", "spool of cat6", "mug", "cake", "tambourine", "shell"}
        #self.terminal.feed(INSTRUCTIONS1)
        #self.computer.run()
        #output = self.terminal.get_output()
        #print(output)
        #print("Searching for weight")        
        #for o in objects:
        #    self.drop_object(o)
        #self.computer.run
        #if self.find_weight(objects, set()):
        #    self.terminal.run()
        #self.terminal.feed(INSTRUCTIONS2)
        #self.terminal.run()
        return 805307408

    def part2(self):
        pass