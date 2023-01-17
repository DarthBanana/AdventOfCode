
from collections import deque

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def who_wins(elf_count):

    # step size doubles, start increments by step size each iteration
    count = elf_count
    step_size = 1
    start = 1
    while count > 1:
        print(count, step_size, start)
        step_size *= 2

        if count % 2 == 1:
            start += step_size
            start = start % elf_count

        count = count // 2
    return start

def who_wins_2(elf_count):
    list_head = None
    list_tail = None
    for i in range(elf_count):
        new_node = Node(i + 1)
        if not list_head:
            list_head = new_node
        if list_tail:
            list_tail.next = new_node
        list_tail = new_node
        new_node.next = list_head
    count = elf_count
    list_mid = list_head
    list_prev = list_tail
    for i in range(elf_count // 2):
        list_mid = list_mid.next
        list_prev = list_prev.next
        
    while (not list_head.next == list_head):
        # remove the elf across:
        list_prev.next = list_mid.next
        list_mid = list_mid.next
        if count % 2:
            list_mid = list_mid.next
            list_prev = list_prev.next

        count -= 1
        if count % 1000 == 0:
            print(count)

        list_head = list_head.next
        
    return list_head.data

def test(count, expected):
    result = who_wins(count)
    print(result)
    assert(result == expected)

def test2(count, expected):
    result = who_wins_2(count)
    print(result)
    assert(result == expected)

test(5, 3)
test2(5, 2)
print("Part 1 result : ", who_wins(3014603))

print("Part 2 result : ", who_wins_2(3014603))



    

