TEST_CONTENT = "10000"
TEST_SIZE = 20

REAL_CONTENT = "11100010111110100"
REAL_SIZE = 272
REAL_SIZE_2 = 35651584

def dragon_curve(string): 
    b = ''.join('0' if c=='1' else '1' for c in reversed(string))
    return '{}0{}'.format(string, b)  
    a = string
    r = reversed(string)
    b = ""
    for c in r:
        if c == '1':
            b = b + '0'
        else:
            b = b + '1'
    
    result = a + "0" + b
    
    return result

def fill_disk(start, size):
    print("Filling Disk")
    data = start
    while len(data) < size:
        print(len(data))        
        data = dragon_curve(data)

    return data[0:size]

def calc_checksum(data):
    print("Calculating Checksum")
    checksum = ""
    while (len(checksum) % 2) == 0:
        checksum = ""
        for i in range(0, len(data), 2):
            
            if data[i] == data[i+1]:
                checksum = checksum + '1'
            else:
                checksum = checksum + '0'
        data = checksum
    return checksum

def do_it(data, size):
    value = fill_disk(data, size)
    return calc_checksum(value)


assert(dragon_curve("1") == "100")
assert(dragon_curve("0") == "001")
assert(dragon_curve("11111") == "11111000000")
assert(dragon_curve("111100001010") == "1111000010100101011110000")

result = fill_disk(TEST_CONTENT, TEST_SIZE)
print(result)
assert(result == "10000011110010000111")
checksum = calc_checksum(result)
print(checksum)
assert(checksum == "01100")

assert(do_it(TEST_CONTENT, TEST_SIZE) == "01100")

print("Part 1: ", do_it(REAL_CONTENT, REAL_SIZE))

print("Part 2: ", do_it(REAL_CONTENT, REAL_SIZE_2))