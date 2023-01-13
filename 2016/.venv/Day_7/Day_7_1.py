import os
import re


def open_file(file):
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    absolute_path = absolute_path + '\\'
    file_path = absolute_path + file
    input_file = open(file_path, "r")
    return input_file


def tls_supported(ip):

    substr_re = re.compile("\[[^\[]*\]")
    good_abba = re.compile(r"(.)((?!\1).)\2\1")
    new_string = ip
    while (True):
        match = substr_re.search(new_string)
        if match == None:
            break
        if good_abba.search(match.group()):
            return False
        new_string = new_string.replace(match.group(), "")

    if good_abba.search(ip):
        print(ip)
        return True

    return False


def get_list_tls_supported(list):
    return [ip for ip in list if tls_supported(ip)]


def get_ip_list_from_file(filename):
    file = open_file(filename)
    result = []
    for line in file.readlines():
        line = line.rstrip('\n')
        result.append(line)
    return result


test_list = ["abba[mnop]qrst", "abcd[bddb]xyyx",
             "aaaa[qwer]tyui", "ioxxoj[asdfgh]zxcvbn"]

assert (tls_supported("abba[mnop]qrst") == True)
assert (tls_supported("abcd[bddb]xyyx") == False)
assert (tls_supported("aaaa[qwer]tyui") == False)

# answer is NOT 65
assert (tls_supported("ioxxoj[asdfgh]zxcvbn") == True)
# print(get_list_tls_supported(test_list))
list = get_ip_list_from_file("real_input.txt")
# print(len(list))
supported_list = get_list_tls_supported(list)
print(len(supported_list))
# print(supported_list)
