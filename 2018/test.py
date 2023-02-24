import sys
sys.path.insert(0, "d:\\git\\AdventOfCode\\2018\\MyModules")
import computer    

class Puzzle(computer.Computer):
    def add(self, a, b):
        
        adder = self.get_value(b)
        self.set_register(a,  self.get_register(a) + adder)
        self.ip += 1
    def set(self, a, b):
        self.set_register(a, self.get_value(b))
        self.ip += 1
    def snd(self, x):
        print("Play sournd ", self.get_value(x))
        self.ip += 1
    def mul(self, x,y):
        self.set_register(x, self.get_register(x) + self.get_value(y))
        self.ip += 1
    def mod(self, x,y):
        self.set_register(x, self.get_register(x) % self.get_value(y))
        self.ip += 1
    def rcv(self, x):
        if not (self.get_value(x) == 0):
            print("received ", self.get_value(x))
        self.ip += 1
    def jgz(self, x, y):
        x_val = self.get_value(x)
        y_val = self.get_value(y)
        if x_val > 0:
            self.ip += y_val
        else:
            self.ip += 1

    



code = """\
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""

puzzle = Puzzle()
puzzle.compile(code)
puzzle.run()
print(puzzle.get_register('a'))
