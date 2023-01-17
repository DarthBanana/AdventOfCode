import re

# Seems like some LCM method should work here, but trying
# brute force first

REAL_INPUT = """\
Disc #1 has 5 positions; at time=0, it is at position 2.
Disc #2 has 13 positions; at time=0, it is at position 7.
Disc #3 has 17 positions; at time=0, it is at position 10.
Disc #4 has 3 positions; at time=0, it is at position 2.
Disc #5 has 19 positions; at time=0, it is at position 9.
Disc #6 has 7 positions; at time=0, it is at position 0."""

REAL_INPUT_2 = """\
Disc #1 has 5 positions; at time=0, it is at position 2.
Disc #2 has 13 positions; at time=0, it is at position 7.
Disc #3 has 17 positions; at time=0, it is at position 10.
Disc #4 has 3 positions; at time=0, it is at position 2.
Disc #5 has 19 positions; at time=0, it is at position 9.
Disc #6 has 7 positions; at time=0, it is at position 0.
Disc #7 has 11 positions; at time=0, it is at position 0."""

TEST_INPUT = """\
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1."""


def parse_input(input_string):
    input_re = re.compile(
        r"Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).")
    discs = []
    for line in input_string.splitlines():
        match = input_re.search(line)
        disc = int(match.groups()[0])
        positions = int(match.groups()[1])
        start = int(match.groups()[2])
        discs.append((disc, positions, start))

    return discs


def get_disc_position_at_drop_time(disc, time):
    num, positions, start = disc
    return (start + (time + num)) % positions


def will_ball_pass(discs, time):
    for disc in discs:
        if get_disc_position_at_drop_time(disc, time):
            return False
    return True


def find_first_drop_time(discs):
    time = 0
    while (not will_ball_pass(discs, time)):
        time += 1

    return time


print(parse_input(TEST_INPUT))

discs = parse_input(TEST_INPUT)
assert (find_first_drop_time(discs) == 5)

discs = parse_input(REAL_INPUT)
print(find_first_drop_time(discs))

discs = parse_input(REAL_INPUT_2)
print(find_first_drop_time(discs))
