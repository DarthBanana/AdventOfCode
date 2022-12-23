use std::{collections::HashMap, ops::Add};

use regex::Regex;

#[derive(Debug)]
enum Tile {
    Open,
    Wall,
    Transporter(Coord, Direction),
}

#[derive(Debug, Clone, Copy)]
enum Step {
    Move(i64),
    Right,
    Left,
}

#[derive(Clone, Copy, Debug)]
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
            row_min: HashMap::new(),
            row_max: HashMap::new(),
            col_min: HashMap::new(),
            col_max: HashMap::new(),
        }
    }
}
struct Face {
    size: i64,
    position: (i64, i64),
}
impl Face {
    fn top_left(&self) -> Coord {
        Coord {
            x: 1 + self.position.0 * self.size,
            y: 1 + self.position.1 * self.size,
        }
    }
    fn top_right(&self) -> Coord {
        Coord {
            x: self.top_left().x + (self.size - 1),
            y: self.top_left().y,
        }
    }
    fn bottom_left(&self) -> Coord {
        Coord {
            x: self.top_left().x,
            y: self.top_left().y + (self.size - 1),
        }
    }
    fn bottom_right(&self) -> Coord {
        Coord {
            x: self.top_left().x + (self.size - 1),
            y: self.top_left().y + (self.size - 1),
        }
    }
}
impl Notes {
    //
    // Side A = (51,1)->(101,51)
    // Side B = (101,1)->(151,51)
    // Side C = (51,51)->(101,101)
    // Side D = (1,101)->(51,151)
    // Side E = (51,101)->(101,151)
    // Side F = (1,151)->(51,201)
    //
    // A > -> B >,     A v -> C v,    *A < -> D >,   *A ^ -> F >
    // *B > -> E <,    * B v -> C <,    B < -> A <,   *B ^ -> F ^
    // *C > -> B ^,     C v -> E v,    *C < -> D v,   C ^ -> A ^
    // D > -> E >,     D v -> F v,    *D < -> A >,   *D ^ -> C >
    // *E > -> B <,     *E V -> F <,    E < -> D <,   E ^ -> C ^
    // *F > -> E ^,     *F v -> B v,    *F < -> A v,   F ^ -> D ^
    //
    //
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

    fn glue_edge(
        &mut self,
        source_start: Coord,
        dest_start: Coord,
        dest_end: Coord,
        start_direction: Direction,
        dest_direction: Direction,
    ) {
        let mut size = 0;
        let offset = match start_direction {
            Direction::Up => Coord { x: 0, y: -1 },
            Direction::Down => Coord { x: 0, y: 1 },
            Direction::Right => Coord { x: 1, y: 0 },
            Direction::Left => Coord { x: -1, y: 0 },
        };
        let source_step = match start_direction {
            Direction::Up => Coord { x: 1, y: 0 },
            Direction::Down => Coord { x: 1, y: 0 },
            Direction::Right => Coord { x: 0, y: 1 },
            Direction::Left => Coord { x: 0, y: 1 },
        };
        let mut dest_step = Coord { x: 0, y: 0 };
        if dest_end.x < dest_start.x {
            size = (dest_start.x - dest_end.x) + 1;
            dest_step.x = -1;
        } else if dest_end.x > dest_start.x {
            size = (dest_end.x - dest_start.x) + 1;
            dest_step.x = 1
        }
        if dest_end.y < dest_start.y {
            size = (dest_start.y - dest_end.y) + 1;
            dest_step.y = -1;
        } else if dest_end.y > dest_start.y {
            size = (dest_end.y - dest_start.y) + 1;
            dest_step.y = 1
        }

        let mut cur_source_position = source_start + offset;
        let mut cur_dest_position = dest_start;

        for _i in 0..size {
            self.map.insert(
                cur_source_position,
                Tile::Transporter(cur_dest_position, dest_direction),
            );
            cur_source_position = cur_source_position + source_step;
            cur_dest_position = cur_dest_position + dest_step;
        }
    }

    fn fold_and_glue(&mut self) {
        if *self.row_min.get(&1).unwrap() < 25 {
            //
            // Test input is 4x4 sides:
            //   A
            // BCD
            //   EF
            //

            let a = Face {
                size: 4,
                position: (2, 0),
            };
            let b = Face {
                size: 4,
                position: (0, 1),
            };
            let c = Face {
                size: 4,
                position: (1, 1),
            };
            let d = Face {
                size: 4,
                position: (2, 1),
            };
            let e = Face {
                size: 4,
                position: (2, 2),
            };
            let f = Face {
                size: 4,
                position: (3, 2),
            };

            // Top edge of A
            self.glue_edge(
                a.top_left(),
                b.top_right(),
                b.top_left(),
                Direction::Up,
                Direction::Down,
            );
            // Left edge of A
            self.glue_edge(
                a.top_left(),
                d.bottom_left(),
                d.top_left(),
                Direction::Left,
                Direction::Right,
            );
            // Right edge of A
            self.glue_edge(
                a.top_right(),
                f.bottom_right(),
                f.top_right(),
                Direction::Right,
                Direction::Left,
            );
            // Top edge of B
            self.glue_edge(
                b.top_left(),
                a.top_right(),
                a.top_left(),
                Direction::Up,
                Direction::Down,
            );
            // Left edge of B
            self.glue_edge(
                b.top_left(),
                f.bottom_right(),
                f.bottom_left(),
                Direction::Left,
                Direction::Up,
            );
            // Bottom edge of B
            self.glue_edge(
                b.bottom_left(),
                e.bottom_right(),
                e.bottom_left(),
                Direction::Down,
                Direction::Up,
            );
            // Top edge of C
            self.glue_edge(
                c.top_left(),
                a.top_left(),
                a.bottom_left(),
                Direction::Up,
                Direction::Right,
            );
            // Bottom edge of C
            self.glue_edge(
                c.bottom_left(),
                e.bottom_right(),
                e.top_left(),
                Direction::Down,
                Direction::Right,
            );
            // Right edge of D
            self.glue_edge(
                d.top_right(),
                f.top_right(),
                f.top_left(),
                Direction::Right,
                Direction::Down,
            );
            // Left edge of E
            self.glue_edge(
                e.top_left(),
                c.bottom_right(),
                c.bottom_left(),
                Direction::Left,
                Direction::Up,
            );
            // Bottom edge of E
            self.glue_edge(
                e.bottom_left(),
                b.bottom_right(),
                b.bottom_left(),
                Direction::Down,
                Direction::Up,
            );
            // Top edge of F
            self.glue_edge(
                f.top_left(),
                d.bottom_right(),
                d.top_right(),
                Direction::Up,
                Direction::Left,
            );
            // Right edge of F
            self.glue_edge(
                f.top_right(),
                a.bottom_right(),
                a.top_right(),
                Direction::Right,
                Direction::Left,
            );
            // Bottom edge of f
            self.glue_edge(
                f.bottom_left(),
                b.bottom_left(),
                b.top_left(),
                Direction::Down,
                Direction::Right,
            )
        } else {
            // Real input is 50x50 sides:
            //  AB
            //  C
            // DE
            // F
            let a = Face {
                size: 50,
                position: (1, 0),
            };
            let b = Face {
                size: 50,
                position: (2, 0),
            };
            let c = Face {
                size: 50,
                position: (1, 1),
            };
            let d = Face {
                size: 50,
                position: (0, 2),
            };
            let e = Face {
                size: 50,
                position: (1, 2),
            };
            let f = Face {
                size: 50,
                position: (0, 3),
            };

            // Top edge of A
            self.glue_edge(
                a.top_left(),
                f.top_left(),
                f.bottom_left(),
                Direction::Up,
                Direction::Right,
            );
            // Left edge of A
            self.glue_edge(
                a.top_left(),
                d.bottom_left(),
                d.top_left(),
                Direction::Left,
                Direction::Right,
            );
            // Top edge of B
            self.glue_edge(
                b.top_left(),
                f.bottom_left(),
                f.bottom_right(),
                Direction::Up,
                Direction::Up,
            );
            // Right edge of B
            self.glue_edge(
                b.top_right(),
                e.bottom_right(),
                e.top_right(),
                Direction::Right,
                Direction::Left,
            );
            // Bottom edge of B
            self.glue_edge(
                b.bottom_left(),
                c.top_right(),
                c.bottom_right(),
                Direction::Down,
                Direction::Left,
            );
            // Left edge of C
            self.glue_edge(
                c.top_left(),
                d.top_left(),
                d.top_right(),
                Direction::Left,
                Direction::Down,
            );
            // Right edge of C
            self.glue_edge(
                c.top_right(),
                b.bottom_left(),
                b.bottom_right(),
                Direction::Right,
                Direction::Up,
            );
            // Top edge of D
            self.glue_edge(
                d.top_left(),
                c.top_left(),
                c.bottom_left(),
                Direction::Up,
                Direction::Right,
            );
            // Left edge of D
            self.glue_edge(
                d.top_left(),
                a.bottom_left(),
                a.top_left(),
                Direction::Left,
                Direction::Right,
            );
            // Right edge of E
            self.glue_edge(
                e.top_right(),
                b.bottom_right(),
                b.top_right(),
                Direction::Right,
                Direction::Left,
            );
            // Bottom edge of E
            self.glue_edge(
                e.bottom_left(),
                f.top_right(),
                f.bottom_right(),
                Direction::Down,
                Direction::Left,
            );
            // Left edge of F
            self.glue_edge(
                f.top_left(),
                a.top_left(),
                a.top_right(),
                Direction::Left,
                Direction::Down,
            );
            // Right edge of F
            self.glue_edge(
                f.top_right(),
                e.bottom_left(),
                e.bottom_right(),
                Direction::Right,
                Direction::Up,
            );
            // Bottom edge of F
            self.glue_edge(
                f.bottom_left(),
                b.top_left(),
                b.top_right(),
                Direction::Down,
                Direction::Down,
            );
        }
    }

    fn print_map(&self) {
        for y in 0..18 {
            for x in 0..18 {
                let tile = self.map.get(&Coord { x: x, y: y });
                if tile.is_none() {
                    print!(" ");
                    continue;
                }
                match tile.unwrap() {
                    Tile::Open => print!("."),
                    Tile::Wall => print!("#"),
                    Tile::Transporter(_, _) => print!("@"),
                }
            }
            print!("\n");
        }
    }
}

#[derive(Default)]
struct Me {
    position: Coord,
    direction: Direction,
}

impl Me {
    fn get_step(&self) -> Coord {
        match self.direction {
            Direction::Up => Coord { x: 0, y: -1 },
            Direction::Down => Coord { x: 0, y: 1 },
            Direction::Right => Coord { x: 1, y: 0 },
            Direction::Left => Coord { x: -1, y: 0 },
        }
    }

    fn move_forward(&mut self, notes: &Notes, dist: i64) {
        for _i in 0..dist {
            let new_coord = self.position + self.get_step();
            //println!("{:?} {:?} -> {:?}", self.position, self.direction, new_coord);
            let tile = notes.map.get(&new_coord).unwrap();
            //println!("{:?}", tile);
            match tile {
                Tile::Open => self.position = new_coord,
                Tile::Wall => return,
                Tile::Transporter(pos, dir) => {
                    //println!("Teleporting from {:?} {:?} to {:?} {:?}", self.position, self.direction, pos, dir);
                    match notes.map.get(pos).unwrap() {
                        Tile::Open => {
                            self.position = *pos;
                            self.direction = *dir;
                        }
                        Tile::Wall => return (),
                        _ => panic!("unexpected tile"),
                    }
                }
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

fn solve_puzzle(input_string: &String) -> i64 {
    let mut notes: Notes = Default::default();
    notes.init_from_string(input_string);
    notes.print_map();
    notes.fold_and_glue();
    notes.print_map();
    let mut me: Me = Default::default();

    me.position.y = 1;
    me.position.x = *notes.row_min.get(&1).unwrap();
    for step in &notes.path {
        me.execute_step(&notes, *step);
    }
    let mut result = match me.direction {
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
    let expected_sample_output = 5031;

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
