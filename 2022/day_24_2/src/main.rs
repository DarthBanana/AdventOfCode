use std::{
    cmp::min,
    collections::{HashMap, HashSet},
    ops::Add,
};

#[derive(Debug, Default, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
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

const UP: Coord = Coord { x: 0, y: -1 };
const RIGHT: Coord = Coord { x: 1, y: 0 };
const DOWN: Coord = Coord { x: 0, y: 1 };
const LEFT: Coord = Coord { x: -1, y: 0 };
const STAY: Coord = Coord { x: 0, y: 0 };

struct Blizzard {
    position: Coord,
    direction: Coord,
}

#[derive(Debug)]
struct State {
    shortest_path: i64,
    history: HashSet<(Coord, i64)>,
    goal: Coord,
}
impl Default for State {
    fn default() -> Self {
        State {
            shortest_path: i64::MAX,
            history: HashSet::new(),
            goal: Default::default(),
        }
    }
}

struct Puzzle {
    map: HashSet<Coord>,
    rows: HashMap<i64, Vec<Blizzard>>,
    columns: HashMap<i64, Vec<Blizzard>>,
    start_coord: Coord,
    end_coord: Coord,
    height: i64,
    width: i64,
}

impl Default for Puzzle {
    fn default() -> Self {
        Puzzle {
            map: HashSet::new(),
            rows: HashMap::new(),
            columns: HashMap::new(),
            start_coord: Default::default(),
            end_coord: Default::default(),
            height: 0,
            width: 0,
        }
    }
}

impl Puzzle {
    fn get_row(&mut self, row: i64) -> &mut Vec<Blizzard> {
        if !self.rows.contains_key(&row) {
            let vec: Vec<Blizzard> = Vec::new();
            self.rows.insert(row, vec);
        }
        self.rows.get_mut(&row).unwrap()
    }

    fn get_col(&mut self, col: i64) -> &mut Vec<Blizzard> {
        if !self.columns.contains_key(&col) {
            let vec: Vec<Blizzard> = Vec::new();
            self.columns.insert(col, vec);
        }
        self.columns.get_mut(&col).unwrap()
    }

    fn init_from_string(&mut self, input_string: &String) {
        let mut y = -2;

        for line in input_string.lines() {
            y = y + 1;

            let mut x = -2;
            self.width = line.len() as i64 - 2;
            for c in line.chars() {
                x = x + 1;
                let coord = Coord { x, y };
                if c != '#' {
                    self.map.insert(coord);
                }
                match c {
                    '^' => self.get_col(x).push(Blizzard {
                        position: coord,
                        direction: UP,
                    }),
                    '>' => self.get_row(y).push(Blizzard {
                        position: coord,
                        direction: RIGHT,
                    }),
                    'v' => self.get_col(x).push(Blizzard {
                        position: coord,
                        direction: DOWN,
                    }),
                    '<' => self.get_row(y).push(Blizzard {
                        position: coord,
                        direction: LEFT,
                    }),
                    _ => (),
                };
            }
        }
        self.height = y;
        self.start_coord = Coord { x: 0, y: -1 };
        self.end_coord = Coord {
            x: self.width - 1,
            y: self.height,
        };
    }

    fn get_moves_for_minute(&self, pos: Coord, minute: i64) -> Vec<Coord> {
        let mut moves: HashSet<Coord> = HashSet::new();
        moves.insert(pos + UP);
        moves.insert(pos + RIGHT);
        moves.insert(pos + LEFT);
        moves.insert(pos + DOWN);
        moves.insert(pos + STAY);

        for col in pos.x - 1..=pos.x + 1 {
            let c = self.columns.get(&col);
            if c.is_none() {
                continue;
            }
            for b in c.unwrap() {
                let new_coord = Coord {
                    x: col,
                    y: ((b.position.y + self.height) + b.direction.y * (minute % self.height))
                        % self.height,
                };
                moves.remove(&new_coord);
            }
        }
        for row in pos.y - 1..=pos.y + 1 {
            let r = self.rows.get(&row);
            if r.is_none() {
                continue;
            }
            for b in r.unwrap() {
                let new_coord = Coord {
                    x: ((b.position.x + self.width) + b.direction.x * (minute % self.width))
                        % self.width,
                    y: row,
                };
                moves.remove(&new_coord);
            }
        }
        let mut moves_vec: Vec<Coord> = Vec::new();
        let mut stay = false;
        for m in moves.drain() {
            if self.map.contains(&m) {
                if m == pos {
                    stay = true;
                    continue;
                }
                moves_vec.push(m);
            }
        }
        if stay {
            moves_vec.push(pos);
        }
        moves_vec.sort();

        moves_vec
    }

    fn find_path(&self, pos: Coord, minute: i64, state: &mut State) {
        if minute > 1000 {
            return;
        }
        //println!("{}: ({},{})", minute, pos.x, pos.y);
        if !state
            .history
            .insert((pos, minute % (self.width * self.height)))
        {
            return;
        }

        if pos == state.goal {
            state.shortest_path = min(minute, state.shortest_path);
            println!("Found Goal : {}", state.shortest_path);
            return;
        }
        let distance_to_end = (state.goal.y - pos.y).abs() + (state.goal.x - pos.x).abs();
        if minute + distance_to_end > state.shortest_path {
            return;
        }

        let mut moves = self.get_moves_for_minute(pos, minute + 1);
        if state.goal == self.end_coord {
            moves.reverse();
        }
        for m in moves {
            self.find_path(m, minute + 1, state);
        }
    }
}

fn solve_puzzle(input_string: &String) -> i64 {
    let mut state: State = Default::default();
    let mut puzzle: Puzzle = Default::default();
    let mut time = 0;
    puzzle.init_from_string(input_string);
    state.goal = puzzle.end_coord;
    println!("Forward");
    puzzle.find_path(puzzle.start_coord, time, &mut state);

    time = state.shortest_path;

    state = Default::default();
    state.goal = puzzle.start_coord;

    println!("Backward");
    puzzle.find_path(puzzle.end_coord, time, &mut state);

    time = state.shortest_path;
    state = Default::default();
    state.goal = puzzle.end_coord;
    println!("Forward");
    puzzle.find_path(puzzle.start_coord, time, &mut state);
    time = state.shortest_path;

    time
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 54;

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
