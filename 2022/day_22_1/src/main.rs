use std::{collections::HashMap, ops::Add};

use regex::Regex;

enum Tile {
    Open,
    Wall,
}

#[derive(Debug, Clone, Copy)]
enum Step {
    Move(i64),
    Right,
    Left,
}

enum Direction {
    Up,
    Down,
    Right,
    Left,
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

impl Default for Direction {
    fn default() -> Self {
        Self::Right
    }
}

struct Notes {
    map: HashMap<Coord, Tile>,
    path: Vec<Step>,
    start_x: i64,
    row_min: HashMap<i64, i64>,
    row_max: HashMap<i64, i64>,
    col_min: HashMap<i64, i64>,
    col_max: HashMap<i64, i64>,
}

impl Default for Notes {
    fn default() -> Self {
        Notes {
            map: HashMap::new(),
            path: Vec::new(),
            start_x: 0,
            row_min: HashMap::new(),
            row_max: HashMap::new(),
            col_min: HashMap::new(),
            col_max: HashMap::new(),
        }
    }
}

#[derive(Default)]
struct Me {
    position: Coord,
    direction: Direction,
}

impl Me {
    fn move_forward(&mut self, notes: &Notes, dist: i64) {
        let (fwd, wrap) = match self.direction {
            Direction::Up => (
                Coord { x: 0, y: -1 },
                Coord {
                    x: self.position.x,
                    y: *notes.col_max.get(&self.position.x).unwrap(),
                },
            ),
            Direction::Down => (
                Coord { x: 0, y: 1 },
                Coord {
                    x: self.position.x,
                    y: *notes.col_min.get(&self.position.x).unwrap(),
                },
            ),
            Direction::Right => (
                Coord { x: 1, y: 0 },
                Coord {
                    x: *notes.row_min.get(&self.position.y).unwrap(),
                    y: self.position.y,
                },
            ),
            Direction::Left => (
                Coord { x: -1, y: 0 },
                Coord {
                    x: *notes.row_max.get(&self.position.y).unwrap(),
                    y: self.position.y,
                },
            ),
        };

        let mut new_coord = self.position;
        for _i in 0..dist {
            new_coord = new_coord + fwd;
            let mut tile = notes.map.get(&new_coord);
            if tile.is_none() {
                new_coord = wrap;
                tile = notes.map.get(&new_coord);
            }
            match tile.unwrap() {
                Tile::Open => self.position = new_coord,
                Tile::Wall => return,
            }
        }
    }

    fn turn_right(&mut self) {
        self.direction = match self.direction {
            Direction::Up => Direction::Right,
            Direction::Down => Direction::Left,
            Direction::Right => Direction::Down,
            Direction::Left => Direction::Up,
        }
    }
    fn turn_left(&mut self) {
        self.direction = match self.direction {
            Direction::Up => Direction::Left,
            Direction::Down => Direction::Right,
            Direction::Right => Direction::Up,
            Direction::Left => Direction::Down,
        }
    }
    fn execute_step(&mut self, notes: &Notes, step: Step) {
        match step {
            Step::Move(dist) => self.move_forward(notes, dist),
            Step::Right => self.turn_right(),
            Step::Left => self.turn_left(),
        }
    }
}

impl Notes {
    fn init_from_string(&mut self, input: &String) {
        let mut y = 0;
        for line in input.lines() {
            if line.contains('R') {
                let re = Regex::new(r"\d+|R|L").unwrap();
                let matches = re.find_iter(line);
                for m in matches {
                    let s = m.as_str();
                    if s.chars().nth(0).unwrap() == 'R' {
                        self.path.push(Step::Right);
                    } else if s.chars().nth(0).unwrap() == 'L' {
                        self.path.push(Step::Left);
                    } else {
                        self.path.push(Step::Move(s.parse().unwrap()));
                    }
                }
            } else {
                y = y + 1;
                let mut x = 0;
                let mut found_first = false;
                for c in line.chars() {
                    x = x + 1;
                    let mut found_cell = false;
                    match c {
                        '.' => {
                            found_cell = true;
                            self.map.insert(Coord { x, y }, Tile::Open);
                        }
                        '#' => {
                            found_cell = true;
                            self.map.insert(Coord { x, y }, Tile::Wall);
                        }
                        _ => (),
                    }
                    if found_cell {
                        if !self.row_min.contains_key(&y) {
                            self.row_min.insert(y, x);
                        }
                        self.row_max.insert(y, x);
                        if !self.col_min.contains_key(&x) {
                            self.col_min.insert(x, y);
                        }
                        self.col_max.insert(x, y);
                    }
                }
            }
        }
    }
}

fn solve_puzzle(input_string: &String) -> i64 {
    let mut result = 0;
    let mut notes: Notes = Default::default();
    notes.init_from_string(input_string);
    let mut me: Me = Default::default();
    me.position.y = 1;
    me.position.x = *notes.row_min.get(&1).unwrap();
    for step in &notes.path {
        me.execute_step(&notes, *step);
    }
    result = match me.direction {
        Direction::Up => 3,
        Direction::Down => 1,
        Direction::Right => 0,
        Direction::Left => 2,
    };
    result += 4 * me.position.x + 1000 * me.position.y;
    result
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 6032;

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
