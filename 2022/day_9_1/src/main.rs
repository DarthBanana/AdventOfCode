use std::collections::HashSet;
#[derive(Debug, Copy, Clone)]
enum Direction {
    Left,
    Right,
    Up,
    Down,
}
#[derive(Hash, Eq, PartialEq, Debug, Copy, Clone)]
struct Position {
    x: i32,
    y: i32,
}

struct Rope {
    head: Position,
    tail: Position,
    tail_history: HashSet<Position>,
}

impl Rope {
    fn move_head_one(&mut self, dir: Direction) {
        match dir {
            Direction::Left => self.head.x -= 1,
            Direction::Right => self.head.x += 1,
            Direction::Up => self.head.y += 1,
            Direction::Down => self.head.y -= 1,
        }
    }
    fn tail_response(&mut self) {
        let x_delta = self.head.x - self.tail.x;
        let y_delta = self.head.y - self.tail.y;

        if x_delta.abs() < 2 && y_delta.abs() < 2 {
            // head and tail are already touching
            return;
        }
        if x_delta != 0 {
            self.tail.x += x_delta / x_delta.abs();
        }

        if y_delta != 0 {
            self.tail.y += y_delta / y_delta.abs();
        }
    }

    fn execute_move(&mut self, dir: Direction, dist: u32) {
        for _i in 0..dist {
            self.move_head_one(dir);
            self.tail_response();
            self.tail_history.insert(self.tail);
        }
    }
}

fn solve_puzzle(input_string: &String) -> u32 {
    let mut rope = Rope {
        head: Position { x: 0, y: 0 },
        tail: Position { x: 0, y: 0 },
        tail_history: HashSet::new(),
    };

    for line in input_string.lines() {
        let (c, dist) = sscanf::sscanf!(line, "{} {}", char, u32).unwrap();
        let dir = match c {
            'R' => Direction::Right,
            'L' => Direction::Left,
            'U' => Direction::Up,
            'D' => Direction::Down,
            _ => panic!("bad input!!!"),
        };
        rope.execute_move(dir, dist);
    }
    let result = rope.tail_history.len() as u32;
    result
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 13;

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
