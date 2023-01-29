## advent of code 2017
## https://adventofcode.com/2017
## day 04


def parse_input(lines):
    return lines


def part1(data):
    count = 0
    for line in data:
        words = line.split()
        word_set = set(words)
        if len(words) == len(word_set):
            count += 1
    return count


def part2(data):
    count = 0
    for line in data:
        words = line.split()
        word_set = set()
        for word in words:
            word_set.add(str(sorted(word)))

        if len(words) == len(word_set):
            print(line)
            count += 1
    return count
