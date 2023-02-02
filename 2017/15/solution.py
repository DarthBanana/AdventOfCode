## advent of code 2017
## https://adventofcode.com/2017
## day 15
STARTA = 289
STARTB = 629

FACTORA = 16807
FACTORB = 48271

DIVISOR = 2147483647


def parse_input(lines):
    pass


def part1(data):
    a = STARTA
    b = STARTB
    sum = 0
    for i in range(40000000):
        a = (a * FACTORA) % DIVISOR
        b = (b * FACTORB) % DIVISOR
        if (a % 65536) == (b % 65536):
            sum += 1

    return sum


def next_a(a):
    while True:
        a = (a * FACTORA) % DIVISOR
        if a % 4 == 0:
            return a


def next_b(b):
    while True:
        b = (b * FACTORB) % DIVISOR
        if b % 8 == 0:
            return b


def part2(data):
    a = STARTA
    b = STARTB
    sum = 0
    for i in range(5000000):
        a = next_a(a)
        b = next_b(b)
        if (a % 65536) == (b % 65536):
            sum += 1
    return sum
