import os


def open_file(file):
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    absolute_path = absolute_path + '\\'
    file_path = absolute_path + file
    input_file = open(file_path, "r")
    return input_file


def get_signal(file):
    input_file = open_file(file)
    maps = []
    first = True
    for line in input_file.readlines():
        if first:
            for i in range(len(line)):
                maps.append({})
            first = False

        for i in range(len(line)):
            count = 0
            c = line[i]
            if c in maps[i]:
                count = maps[i][c]

            maps[i][c] = count + 1
    signal = ""
    for map in maps:
        map_list = list(map.items())
        map_list.sort(key=lambda x: x[1])
        map_list.reverse()
        signal += map_list[0][0]

    return signal


print(get_signal("test_data.txt"))
print(get_signal("real_data.txt"))
