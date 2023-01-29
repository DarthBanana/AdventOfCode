## advent of code 2017
## https://adventofcode.com/2017
## day 09

import re


def parse_input(lines):
    print(len(lines))
    return lines[0]


cancel_re = re.compile(r"!.")
garbage_re = re.compile(r"\<([^\>]*)>")
braces_re = re.compile(r"[^\{\}]")


def part1(data):
    # print(data)
    new_string = cancel_re.sub("", data)

    # print(new_string)
    new_string = garbage_re.sub("", new_string)
    # print(new_string)
    new_string = braces_re.sub("", new_string)
    # print(new_string)
    total_score = 0
    depth = 0
    for c in new_string:
        if c == "{":
            depth += 1
            total_score += depth
        elif c == "}":
            depth -= 1
    return total_score


def part2(data):
    new_string = cancel_re.sub("", data)

    total = 0
    for match in garbage_re.finditer(new_string):
        total += len(match.group(1))

    return total
