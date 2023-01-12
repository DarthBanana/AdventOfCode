import os

def is_valid_triangle(sides):
    sides.sort()
    return sides[0] + sides[1] > sides[2]

def read_columns(file):
    columns = [[],[],[]]

    absolute_path = os.path.dirname(os.path.abspath(__file__))
    file_path = absolute_path + file
    input_file = open(file_path, "r")
    count = 0
    for line in input_file.readlines():
        col = 0
    
        line = line.strip()
        for n in line.split():        
            columns[col].append(int(n))
            col += 1
    
    return columns

def read_triangles(file):
    triangles = []
    columns = read_columns(file)
    for col in columns:
        while len(col):
            triangle = []
            triangle.append(col.pop())
            triangle.append(col.pop())
            triangle.append(col.pop())
            triangles.append(triangle)
        
    return triangles
        

print(is_valid_triangle([5, 10, 25]))
triangles = read_triangles("\Day_3_test.txt")
#print(triangles)


triangles = read_triangles("\Day_3_input.txt")
#print(triangles)
count = 0
for triangle in triangles:
    
    if is_valid_triangle(triangle):
        count += 1
        
print(count)

