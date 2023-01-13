import os
import re


def open_file(file):
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    absolute_path = absolute_path + '\\'
    file_path = absolute_path + file
    input_file = open(file_path, "r")
    return input_file

def decompress(compressed_text):
    print(compressed_text)
    
    marker = re.compile(r"\((\d+)x(\d+)\)")    
    new_string = ""
    last_index = 0
    while(True):
        match = marker.search(compressed_text)
        if match == None:
            new_string += compressed_text
            print(new_string)
            return new_string
        
        
        new_string = new_string + compressed_text[0:match.span()[0]]
        repeat_length = int(match.group(1))
        repeat_count = int(match.group(2))
        for i in range(repeat_count):
            new_string += compressed_text[match.span()[1]:match.span()[1] + repeat_length]
        
        compressed_text = compressed_text[match.span()[1] + repeat_length:]

def calc_decompress_len(compressed_text):
    marker = re.compile(r"\((\d+)x(\d+)\)") 
    match = marker.search(compressed_text)
    if match == None:
        return len(compressed_text)

    repeat_length = int(match.group(1))
    repeat_count = int(match.group(2))
    length = match.span()[0] + repeat_length*repeat_count
    length += calc_decompress_len(compressed_text[match.span()[1]+repeat_length:])
    return length





def test():
    assert decompress("ADVENT") == "ADVENT"
    assert decompress("A(1x5)BC") == "ABBBBBC"
    assert decompress("(3x3)XYZ") == "XYZXYZXYZ"
    assert decompress("A(2x2)BCD(2x2)EFG") == "ABCBCDEFEFG"
    assert decompress("(6x1)(1x3)A") == "(1x3)A"
    assert decompress("X(8x2)(3x3)ABCY") == "X(3x3)ABC(3x3)ABCY"


def run():
    file = open_file("input.txt")
    data = file.readline()
    result = decompress(data)
    print(len(result))
    print(calc_decompress_len(data))
    
    return len(result)


test()

print(run())
