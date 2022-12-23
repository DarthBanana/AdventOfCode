use std::{
    cmp::{max, min},
    collections::{HashSet, VecDeque},
    ops::Add,
};

const NW: Coord = Coord { x: -1, y: -1 };
const N: Coord = Coord { x: 0, y: -1 };
const NE: Coord = Coord { x: 1, y: -1 };
const E: Coord = Coord { x: 1, y: 0 };
const SE: Coord = Coord { x: 1, y: 1 };
const S: Coord = Coord { x: 0, y: 1 };
const SW: Coord = Coord { x: -1, y: 1 };
const W: Coord = Coord { x: -1, y: 0 };

const DIRECTIONS: [Coord; 8] = [NW, N, NE, E, SE, S, SW, W];

#[derive(Debug, Default, Clone, PartialEq, Eq, Hash)]
struct Move {
    move_direction: Coord,
    check_first: Vec<Coord>,
}

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

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct Elf {
    position: Coord,
    proposed_move: Option<Coord>,
}

#[derive(Debug, Default, Clone)]
struct Puzzle {
    elves: Vec<Elf>,
    move_priorities: VecDeque<Move>,
    map: HashSet<Coord>,
}

impl Puzzle {
    fn init_from_string(&mut self, input_string: &String) {
        let mut y = 0;

        for line in input_string.lines() {
            let mut x = 0;
            for c in line.chars() {
                if c == '#' {
                    let elf = Elf {
                        position: Coord { x: x, y: y },
                        proposed_move: None,
                    };
                    self.elves.push(elf);
                    self.map.insert(elf.position);
                }
                x += 1;
            }
            y = y + 1;
        }

        self.move_priorities.push_back(Move {
            move_direction: N,
            check_first: vec![NW, N, NE],
        });
        self.move_priorities.push_back(Move {
            move_direction: S,
            check_first: vec![SW, S, SE],
        });
        self.move_priorities.push_back(Move {
            move_direction: W,
            check_first: vec![NW, W, SW],
        });
        self.move_priorities.push_back(Move {
            move_direction: E,
            check_first: vec![NE, E, SE],
        });
    }

    fn execute_step(&mut self) -> bool {
        let mut elf_moved = false;
        let mut proposed_moves: HashSet<Coord> = HashSet::new();
        let mut conflicting_moves: HashSet<Coord> = HashSet::new();
        //
        // Phase 1:
        //
        for elf in self.elves.iter_mut() {
            let mut stay_put = true;
            //
            // See if elf should stay put
            //
            for d in DIRECTIONS {
                if self.map.contains(&(elf.position + d)) {
                    stay_put = false;
                    break;
                }
            }
            if stay_put {
                continue;
            }

            for m in self.move_priorities.iter() {
                let mut move_ok = true;
                for d in m.check_first.iter() {
                    if self.map.contains(&(elf.position + *d)) {
                        move_ok = false;
                        break;
                    }
                }
                if move_ok {
                    let proposed_move = elf.position + m.move_direction;

                    let unique = proposed_moves.insert(proposed_move);
                    if !unique {
                        conflicting_moves.insert(proposed_move);
                    }
                    elf.proposed_move = Some(proposed_move);

                    break;
                }
            }
        }

        //
        // Phase 2:
        //
        for elf in self.elves.iter_mut() {
            if elf.proposed_move.is_none() {
                continue;
            }
            let proposed_move = elf.proposed_move.unwrap();
            elf.proposed_move = None;
            if conflicting_moves.contains(&proposed_move) {
                continue;
            }
            self.map.remove(&elf.position);
            self.map.insert(proposed_move);
            elf.position = proposed_move;
            elf_moved = true;
        }

        let m = self.move_priorities.pop_front().unwrap();
        self.move_priorities.push_back(m);
        elf_moved
    }

    fn calculate_score(&self) -> i64 {
        //
        // First find the rectangle
        //
        let mut min_x = i64::MAX;
        let mut min_y = i64::MAX;
        let mut max_x = i64::MIN;
        let mut max_y = i64::MIN;
        for elf in self.elves.iter() {
            min_x = min(min_x, elf.position.x);
            min_y = min(min_y, elf.position.y);
            max_x = max(max_x, elf.position.x);
            max_y = max(max_y, elf.position.y);
        }

        let area = ((max_x + 1) - min_x) * ((max_y + 1) - min_y);
        let empty_locations = area - self.elves.len() as i64;

        empty_locations
    }

    fn print_map(&self) {
        //
        // First find the rectangle
        //
        let mut min_x = i64::MAX;
        let mut min_y = i64::MAX;
        let mut max_x = i64::MIN;
        let mut max_y = i64::MIN;
        for elf in self.elves.iter() {
            min_x = min(min_x, elf.position.x);
            min_y = min(min_y, elf.position.y);
            max_x = max(max_x, elf.position.x);
            max_y = max(max_y, elf.position.y);
        }

        for y in min_y..=max_y {
            for x in min_x..=max_x {
                if self.map.contains(&Coord { x, y }) {
                    print!("#");
                } else {
                    print!(".");
                }
            }
            print!("\n");
        }
        print!("\n\n");
    }
}

fn solve_puzzle(input_string: &String) -> i64 {
    let mut puzzle: Puzzle = Default::default();
    puzzle.init_from_string(input_string);
    puzzle.print_map();
    let mut round = 0;
    loop {
        round += 1;
        if !puzzle.execute_step() {
            break;
        }
    }
    round
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 20;

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
    let result = solve_puzzle(&test_input_string);
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
    let result = solve_puzzle(&real_input_string);
    println!("Real Result : {}", result);
}
