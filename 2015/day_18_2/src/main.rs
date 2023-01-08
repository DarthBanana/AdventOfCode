use std::{collections::HashMap, ops::Add};

const NW: Coord = Coord { x: -1, y: -1 };
const N: Coord = Coord { x: 0, y: -1 };
const NE: Coord = Coord { x: 1, y: -1 };
const E: Coord = Coord { x: 1, y: 0 };
const SE: Coord = Coord { x: 1, y: 1 };
const S: Coord = Coord { x: 0, y: 1 };
const SW: Coord = Coord { x: -1, y: 1 };
const W: Coord = Coord { x: -1, y: 0 };

const DIRECTIONS: [Coord; 8] = [NW, N, NE, E, SE, S, SW, W];

#[derive(Debug, Default, Clone, Copy, PartialEq, Eq, Hash)]
struct Coord {
    x: i64,
    y: i64,
}

impl Add for Coord {
    type Output = Coord;

    fn add(self, other: Coord) -> Coord {
        Coord {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

struct Puzzle {
    lights: HashMap<Coord, bool>,
    corners: Vec<Coord>,
    max_x: i64,
    max_y: i64,
}

impl Puzzle {
    fn init_from_string(&mut self, input_string: &String) {
        let mut coord = Coord { x: 0, y: 0 };

        for line in input_string.lines() {
            coord.x = 0;

            for c in line.chars() {
                match c {
                    '.' => {
                        self.lights.insert(coord, false);
                    }
                    '#' => {
                        self.lights.insert(coord, true);
                    }
                    _ => (),
                };
                coord.x += 1;
            }
            coord.y += 1;
        }

        self.corners.push(Coord { x: 0, y: 0 });
        self.corners.push(Coord {
            x: 0,
            y: coord.y - 1,
        });
        self.corners.push(Coord {
            x: coord.x - 1,
            y: 0,
        });
        self.corners.push(Coord {
            x: coord.x - 1,
            y: coord.y - 1,
        });
        self.max_x = coord.x - 1;
        self.max_y = coord.y - 1;
    }
    fn run_step(&mut self) {
        let mut turn_on: Vec<Coord> = Vec::new();
        let mut turn_off: Vec<Coord> = Vec::new();
        for (light, state) in self.lights.iter() {
            let mut neighbor_count = 0;
            //
            // How many neighbors are on?
            //
            for d in DIRECTIONS {
                let neighbor = *light + d;
                let res = self.lights.get(&neighbor);
                match res {
                    Some(x) => {
                        if *x {
                            neighbor_count += 1;
                        }
                    }
                    None => (),
                }
            }
            if *state {
                if neighbor_count == 2 || neighbor_count == 3 {
                    // stay on
                } else {
                    turn_off.push(*light);
                }
            } else {
                if neighbor_count == 3 {
                    turn_on.push(*light);
                }
            }
        }

        //
        // Now flip the lights
        //
        for light in turn_on.drain(..) {
            self.lights.insert(light, true);
        }
        for light in turn_off.drain(..) {
            self.lights.insert(light, false);
        }
        for light in self.corners.iter() {
            self.lights.insert(*light, true);
        }
    }

    fn print_lights(&self) {
        println!("");
        for y in 0..=self.max_y {
            println!("");
            for x in 0..=self.max_x {
                let coord = Coord { x, y };
                let val = self.lights.get(&coord).unwrap();
                if *val {
                    print!("#");
                } else {
                    print!(".");
                }
            }
        }
    }
    fn count_ons(&self) -> u32 {
        let mut count = 0;
        for (_light, state) in self.lights.iter() {
            if *state {
                count += 1;
            }
        }
        count
    }
}

fn solve_puzzle(input_string: &String, steps: u32) -> u32 {
    let mut puzzle: Puzzle = Puzzle {
        lights: HashMap::new(),
        corners: Vec::new(),
        max_x: 0,
        max_y: 0,
    };

    puzzle.init_from_string(input_string);

    for _i in 0..steps {
        puzzle.run_step();
    }

    puzzle.count_ons()
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 17;

    //
    // Print the specific puzzle info
    //
    let (day, part) = sscanf::sscanf!(env!("CARGO_PKG_NAME"), "day_{}_{}", u32, u32).unwrap();
    println!("Day {} : Part {}!", day, part);

    //
    // Read in the sample input
    //
    let test_input_string = std::fs::read_to_string(
        std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("sample.txt"),
    )
    .unwrap();

    //
    // Read in the real input
    //
    let real_input_string =
        std::fs::read_to_string(std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("input.txt"))
            .unwrap();

    //
    // Solve for the sample input
    //
    println!("Testing Sample Data:");
    let result = solve_puzzle(&test_input_string, 5);
    println!("Sample Result : {}", result);

    //
    // Check if the sample input matches the expected result
    //
    if result != expected_sample_output {
        println!("Wrong Answer!!!!! {}", result);
        return;
    }

    //
    // Solve for the real input, only in the case that the result
    // for the sample input was correct
    //
    println!("Testing Real Data:");
    let result = solve_puzzle(&real_input_string, 100);
    println!("Real Result : {}", result);
}
