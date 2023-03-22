## advent of code 2019
## https://adventofcode.com/2019
## day 23
import signal
import sys
from intcode import *
from aocpuzzle import *
from threaded_computer import *

class Packet():
    def __init__(self, x, y, address, source):
        self.x = x
        self.y = y
        self.address = address
        self.source = source
    def __str__(self):
        return f"{self.source} -> ({self.x}, {self.y}) -> {self.address}"

class CableFromComputer(Mailbox):
    def __init__(self, router, id, cable_to_computer):
        self.router = router
        self.id = id        
        self.cable_to_computer = cable_to_computer
        super().__init__()    

    def send(self, value: int):
        self.cable_to_computer.reset_idle
        super().send(value)
        #print("<", self.id, value, ">")
        if len(self.mailbox) >= 3:
            addr = self.mailbox.popleft()
            x = self.mailbox.popleft()
            y = self.mailbox.popleft()
           
            packet = Packet(x, y, addr, self.id)
            #print("Computer", self.id, "sending packet to ", addr)
            self.router.send_packet(packet)

class CableToComputer(Mailbox):
    def __init__(self, id, verbose = False):
        self.id = id        
        self.empty_count = 0
        self.idle_lock = threading.Lock()
        super().__init__(verbose)

    def reset_idle(self):
        self.idle_lock.acquire()
        self.empty_count = 0
        self.idle_lock.release()

    def is_idle(self):
        self.idle_lock.acquire()
        result = self.empty_count > 10
        self.idle_lock.release()
        return result

    def reset(self):
        super().reset()
        self.mailbox.append(self.id)
    
    def receive(self):
        #print(self.id, "receive")
        if len(self.mailbox) == 0:
            self.idle_lock.acquire()
            self.empty_count += 1
            self.idle_lock.release()
            return -1
        self.reset_idle()
        return super().receive()
    
    def send_packet(self, packet):
        self.reset_idle()
        #print("Sending packet to ", self.id)
        self.mailbox.append(packet.x)
        self.mailbox.append(packet.y)
    def __len__(self):
        return 100

class Connection():
    def __init__(self):
        self.to_computer = None
        self.from_computer = None
        self.computer = None
        self.thread = None

class Router():
    def __init__(self):
        self.incoming_packets = deque()
        self.connections = []        
        self.rcv_event = threading.Event()
        self.start_event = threading.Event()
        self.nat_packet = None
        self.last_nat_packet_sent = None

    def spawn_computer(self):
        id = len(self.connections)
        connection = Connection()
        connection.to_computer = CableToComputer(id)
        connection.from_computer = CableFromComputer(self, id, connection.to_computer)
        print(connection.to_computer.id)
        connection.computer = MyIntcodeComputer(connection.to_computer, connection.from_computer)
        connection.thread = ThreadedComputerEnvironment(connection.computer, str(id), self.start_event)

        self.connections.append(connection)
        return connection.computer
    
    def spawn_computers(self, count):
        for i in range(count):
            self.spawn_computer()

    def send_packet(self, packet):
        self.incoming_packets.append(packet)
        self.rcv_event.set()
    
    def load_program_in_all_computers(self, lines):
        for c in self.connections:
            c.computer.load_program_from_input(lines)
    
    def reset_all_computers(self):
        for c in self.connections:
            c.computer.reset()

    def is_idle(self):
        for c in self.connections:
            if not c.to_computer.is_idle():
                return False
        return True
    
    def nat_packet_received(self, packet):
        self.nat_packet = packet

    def send_nat_packet(self):
        if self.nat_packet is None:
            return
        if self.last_nat_packet_sent is not None:
            if self.nat_packet.y == self.last_nat_packet_sent.y:
                print("Y value repeated:", self.nat_packet.y)
                return self.nat_packet.y
        self.last_nat_packet_sent = self.nat_packet
        self.connections[0].to_computer.send_packet(self.nat_packet)
        self.nat_packet = None

        
    def run_network(self):
        #for c in self.connections:
        #    c.thread.run_on_signal()
        print("Starting network")
        self.start_event.set()
        while(True):
            for c in self.connections:
                c.computer.run(instruction_count=5)
            #self.rcv_event.wait()
            #self.rcv_event.clear()
            while len(self.incoming_packets) > 0:
                packet = self.incoming_packets.popleft()
                print(packet)
                if 0 <= packet.address < len(self.connections):                    
                    self.connections[packet.address].to_computer.send_packet(packet)                
                else:                             
                    yield packet
                    

    def run_network2(self):
        #for c in self.connections:
        #    c.thread.run_on_signal()
        print("Starting network")
        self.start_event.set()
        while(True):
            for c in self.connections:
                c.computer.run(instruction_count=5)            
            while len(self.incoming_packets) > 0:
                packet = self.incoming_packets.popleft()
                print(packet)
                if 0 <= packet.address < len(self.connections):                    
                    self.connections[packet.address].to_computer.send_packet(packet)                
                else:         
                    if packet.address == 255:
                        self.nat_packet_received(packet)
            
            if self.is_idle():
                res = self.send_nat_packet()
                if res is not None:
                    return res        
    


class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.router = Router()
        self.router.spawn_computers(50)
        self.router.load_program_in_all_computers(lines)  

    

    def part1(self):
        self.router.reset_all_computers()
        for packet in self.router.run_network():
            print("main thread received packet", packet.x, packet.y, packet.address)
            if packet.address == 255:
                return packet.y
    
    def part2(self):
        print("part2")
        self.router.reset_all_computers()
        res = self.router.run_network2()
        print(res)
        return res
        