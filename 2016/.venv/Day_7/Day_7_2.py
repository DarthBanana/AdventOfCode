import os
import re


def open_file(file):
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    absolute_path = absolute_path + '\\'
    file_path = absolute_path + file
    input_file = open(file_path, "r")
    return input_file


def ssl_supported(ip):
    hypernets = []
    substr_re = re.compile("\[[^\[]*\]")
    aba = re.compile(r"(?=(.)((?!\1).)\1)")
    new_string = ip
    while (True):
        match = substr_re.search(new_string)
        if match == None:
            break
        hypernets.append(match.group())
        
        new_string = new_string.replace(match.group(), "..")    
    
    superset = aba.findall(new_string)    
    
    return any(b + a + b in h for a,b in superset for h in hypernets)


def get_list_ssl_supported(list):
    return [ip for ip in list if ssl_supported(ip)]


def get_ip_list_from_file(filename):
    file = open_file(filename)
    result = []
    for line in file.readlines():
        line = line.rstrip('\n')
        result.append(line)
    return result


test_list = ["abba[mnop]qrst", "abcd[bddb]xyyx",
             "aaaa[qwer]tyui", "ioxxoj[asdfgh]zxcvbn"]

#assert (ssl_supported("aba[bab]xyz") == True)
assert (ssl_supported("xyx[xyx]xyx") == False)
assert (ssl_supported("aaa[kek]eke") == True)
assert (ssl_supported("zazbz[bzb]cdb") == True)

# answer is NOT 65
#assert (tls_supported("ioxxoj[asdfgh]zxcvbn") == True)
# print(get_list_tls_supported(test_list))
list = get_ip_list_from_file("real_input.txt")
# print(len(list))
supported_list = get_list_ssl_supported(list)
print(len(supported_list))
# print(supported_list)
