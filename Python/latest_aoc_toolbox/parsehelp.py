
import re


def get_int_per_line(lines):
    result = []
    for line in lines:
        newline = line.strip()
        newline = newline.replace("+", "")
        value = int(newline)
        result.append(value)
    return result

def get_ints_per_line(lines):
    lists = []
    for line in lines:
        nums = []
        split = line.split()
        for n in split:
            nums.append(int(n))
        lists.append(nums)

    if len(lists) == 1:
        return lists[0]
    return lists

int_re = re.compile(r"[-+]?\d+")
def get_all_ints(line):    
    return [int(x) for x in int_re.findall(line)]
