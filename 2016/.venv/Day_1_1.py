real_data = "R4, R4, L1, R3, L5, R2, R5, R1, L4, R3, L5, R2, L3, L4, L3, R1, R5, R1, L3, L1, R3, L1, R2, R2, L2, R5, L3, L4, R4, R4, R2, L4, L1, R5, L1, L4, R4, L1, R1, L2, R5, L2, L3, R2, R1, L194, R2, L4, R49, R1, R3, L5, L4, L1, R4, R2, R1, L5, R3, L5, L4, R4, R4, L2, L3, R78, L5, R4, R191, R4, R3, R1, L2, R1, R3, L1, R3, R4, R2, L2, R1, R4, L5, R2, L2, L4, L2, R1, R2, L3, R5, R2, L3, L3, R3, L1, L1, R5, L4, L4, L2, R5, R1, R4, L3, L5, L4, R5, L4, R5, R4, L3, L2, L5, R4, R3, L3, R1, L5, R5, R1, L3, R2, L5, R5, L3, R1, R4, L5, R4, R2, R3, L4, L5, R3, R4, L5, L5, R4, L4, L4, R1, R5, R3, L1, L4, L3, L4, R1, L5, L1, R2, R2, R4, R4, L5, R4, R1, L1, L1, L3, L5, L2, R4, L3, L5, L4, L1, R3"
turns = {'L' : -1, 'R' : 1}
directions = [(0,-1), (1,0), (0,1), (-1,0)]
class Position:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction_index = 0
        
    def turn(self, turn_cmd) :        
        self.direction_index = (self.direction_index + turns[turn_cmd]) % len(directions)
    
    def move_fwd(self, distance) :
        (dx,dy) = directions[self.direction_index]
        self.x = self.x + dx * distance
        self.y = self.y + dy * distance

    def distance_away(self) :
        return abs(self.x) + abs(self.y)

def solve(directions):
    position = Position()
    commands = directions.split(', ',-1)
    for cmd in commands:        
        turn_cmd = cmd[0]
        fwd = int(cmd[1:])        
        position.turn(turn_cmd)
        position.move_fwd(fwd)
    
    return position.distance_away()


result = solve(real_data)
print(result)
