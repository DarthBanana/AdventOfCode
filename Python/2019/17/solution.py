# advent of code 2019
# https://adventofcode.com/2019
# day 17


from time import sleep
from aocpuzzle import *
from PrettyMap2D import *
from intcode import *
from parsehelp import *


class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.always_run_part_1 = True        

        self.input_mailbox = Mailbox()
        self.output_mailbox = Mailbox()
        self.computer = MyIntcodeComputer(
            self.input_mailbox, self.output_mailbox)
        self.computer.load_program_from_input(lines)
        # self.computer[0] = 2
        # self.computer.interpret_program()
        # assert(False)
        #self.map = PrettyMap2D()
        self.map = Map2D()
        self.visited_layer = self.map.add_overlay(100)
        self.reset()
        self.pois = []
        self.last_value = 0
        self.x = 0
        self.y = 0

    def reset(self):
        self.computer.reset()
        self.map.clear()

    def find_path(self):
        robot_position = self.map.find("^")
        robot_direction = N
        path = []
        straight_length = 0
        while True:
            if self.map[robot_position + robot_direction] == "#":
                straight_length += 1
                robot_position += robot_direction
            elif self.map[robot_position + turn_left(robot_direction)] == "#":
                if straight_length > 0:
                    path.append(straight_length)
                    straight_length = 0
                path.append("L")
                robot_direction = turn_left(robot_direction)
            elif self.map[robot_position + turn_right(robot_direction)] == "#":
                if straight_length > 0:
                    path.append(straight_length)
                    straight_length = 0
                path.append("R")
                robot_direction = turn_right(robot_direction)
            else:
                if straight_length > 0:
                    path.append(straight_length)
                return path

    def part1(self):
        self.computer.run()
        x = 0
        y = 0
        self.map.autodraw = False
        while len(self.output_mailbox) > 0:
            value = self.output_mailbox.receive()
            if value == 10:
                y += 1
                x = 0
                continue
            self.map[Coord2D(x, y)] = chr(value)
            x += 1

        self.all_intersections = []
        intersections = []
        for point in self.map:
            if self.map[point] == "#":
                is_point = True
                for neighbor in point.neighbors():
                    if self.map[neighbor] != "#":
                        is_point = False

                if is_point:
                    intersections.append(point)

        total = 0
        for i in intersections:
            total += i.x * i.y

        self.map.refresh()
        return total

    def output_received(self, mailbox, value):
        self.last_value = value

        if value > 127:
            print("BIG VALUE ", value)
            return
        if value == 10:
            if (self.x == 0):
                self.map.refresh()
                self.y = 0
            else:
                self.y += 1

            self.x = 0
            return
        self.map[Coord2D(self.x, self.y)] = chr(value)
        self.x += 1

    def part2(self):
        a_routine = "L,4,L,4,L,10"
        b_routine = "L,4,R,8,L,6,L,10"
        c_routine = "L,6,R,8,R,10,L,6,L,6"
        a_re = re.compile(a_routine)
        b_re = re.compile(b_routine)
        c_re = re.compile(c_routine)
        # self.computer.enable_execution_trace()

        path = self.find_path()
        pathstring = ""
        for e in path:
            pathstring += str(e) + ','
        pathstring = pathstring[:-1]

        pathstring = a_re.sub("A", pathstring)
        pathstring = b_re.sub("B", pathstring)
        pathstring = c_re.sub("C", pathstring)

        self.computer.reset()
        self.computer[0] = 2
        # self.computer.set_breakpoint(327)
        # self.computer.set_breakpoint(184)
        # self.computer.set_breakpoint(1157)

        self.x = 0
        self.y = 0
        self.map.autodraw = True

        # self.computer.run()
        for c in pathstring:
            self.input_mailbox.send(ord(c))
        self.input_mailbox.send(10)

        # self.computer.run()
        for c in a_routine:
            self.input_mailbox.send(ord(c))
        self.input_mailbox.send(10)

        # self.computer.run()
        for c in b_routine:
            self.input_mailbox.send(ord(c))
        self.input_mailbox.send(10)
        self.computer.run()

        # self.computer.run()
        for c in c_routine:
            self.input_mailbox.send(ord(c))
        self.input_mailbox.send(10)

        # self.computer.run()
        draw_em = False
        if draw_em:
            self.input_mailbox.send(ord("y"))
            self.output_mailbox.set_receive_routine(self.output_received)
            drain_mailbox = False
        else:
            self.input_mailbox.send(ord("n"))
            self.output_mailbox.set_receive_routine(self.output_received)
            drain_mailbox = False
        self.input_mailbox.send(10)

        self.x = 0
        self.y = 0
        self.output_mailbox.reset()

        self.computer.autodraw = False
        self.computer.run()
        print(self.computer.can_continue())
        if (self.computer.can_continue()):
            print("still can run??")

        self.map.refresh()
        #sleep(2)
        if drain_mailbox:
            print(len(self.output_mailbox))
            print(self.output_mailbox)
            result = self.output_mailbox.receive()
        else:
            # assert (self.computer.can_continue() == False)
            result = self.last_value
        self.output_mailbox.verbose = True
        self.computer.run()

        # 684691
        return result
