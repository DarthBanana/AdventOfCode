from PrettyMap2D import *


print("Hello World!")
grid = PrettyInfiniteGrid()
grid[Coord2D(6, 6)] = 1
grid[Coord2D(4, 4)] = 2
grid.refresh()
while(True):
    grid.refresh()
    