import os

def is_valid_triangle(sides):
    sides.sort()
    return sides[0] + sides[1] > sides[2]

print(is_valid_triangle([5, 10, 25]))

absolute_path = os.path.dirname(os.path.abspath(__file__))
file_path = absolute_path + "\Day_3_input.txt"
input_file = open(file_path, "r")
count = 0
for line in input_file.readlines():
    
    triangle = []
    line = line.strip()
    for n in line.split():        
        triangle.append(int(n))
    
    if is_valid_triangle(triangle):
        count += 1
        
print(count)

