## advent of code 2017
## https://adventofcode.com/2017
## day 20

import re

PART_ONE = False


def add_em(a, b):
    return tuple(x + y for x, y in zip(a, b))


particle_re = re.compile(
    r"p=\<(-?\d+),(-?\d+),(-?\d+)\>, v=\<(-?\d+),(-?\d+),(-?\d+)\>, a=\<(-?\d+),(-?\d+),(-?\d+)\>"
)


class Particle:
    def __init__(self, id, line):
        match = particle_re.search(line)
        self.id = id
        self.starting_position = (
            int(match.group(1)),
            int(match.group(2)),
            int(match.group(3)),
        )
        self.starting_velocity = (
            int(match.group(4)),
            int(match.group(5)),
            int(match.group(6)),
        )
        self.acceleration = (
            int(match.group(7)),
            int(match.group(8)),
            int(match.group(9)),
        )
        self.current_position = self.starting_position
        self.current_velocity = self.starting_velocity

    def acceleration_magnitude(self):
        return (
            abs(self.acceleration[0])
            + abs(self.acceleration[1])
            + abs(self.acceleration[2])
        )

    def tick(self):
        self.current_velocity = add_em(self.current_velocity, self.acceleration)
        self.current_position = add_em(self.current_position, self.current_velocity)
        return self.current_position


class Puzzle:
    def __init__(self, lines):
        self.particles = []
        id = 0
        for line in lines:
            self.particles.append(Particle(id, line))
            id += 1

    def find_closest_particle(self):
        min = 1000000
        mins = []
        for p in self.particles:
            accel = p.acceleration_magnitude()
            print(p.id, accel)
            if accel < min:
                mins = [p.id]
                min = accel
            elif accel == min:
                mins.append(p.id)
        assert len(mins) == 1
        return mins[0]

    def find_remaining(self):
        uncollided_particles = set()
        for i in range(len(self.particles)):
            uncollided_particles.add(i)

        for i in range(1000):

            seen = {}
            collided_particles = set()
            for id in uncollided_particles:
                p = self.particles[id]
                pos = p.tick()
                if pos in seen.keys():
                    collided_particles.add(seen[pos])
                    collided_particles.add(id)
                else:
                    seen[pos] = id

            if len(collided_particles) > 0:
                uncollided_particles -= collided_particles
        return len(uncollided_particles)


def parse_input(lines):
    return Puzzle(lines)


def part1(puzzle):
    if PART_ONE:
        # I think just find the one with the lowest absolute acceleration value
        return puzzle.find_closest_particle()
    else:
        return 1


def part2(puzzle):
    return puzzle.find_remaining()
