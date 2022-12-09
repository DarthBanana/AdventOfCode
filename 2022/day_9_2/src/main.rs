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

impl Default for Position {
    fn default() -> Self {
        Position { x: 0, y: 0 }
    }
}
#[derive(Debug)]
struct Rope {
    knots: [Position; 10],
    tail_history: HashSet<Position>,
}

impl Rope {
    fn move_head_one(&mut self, dir: Direction) {
        match dir {
            Direction::Left => self.knots[0].x -= 1,
            Direction::Right => self.knots[0].x += 1,
            Direction::Up => self.knots[0].y += 1,
            Direction::Down => self.knots[0].y -= 1,
        }
    }
    fn tail_response(&mut self, knot_index: usize) {
        let x_delta = self.knots[knot_index - 1].x - self.knots[knot_index].x;
        let y_delta = self.knots[knot_index - 1].y - self.knots[knot_index].y;

        if x_delta.abs() < 2 && y_delta.abs() < 2 {
            // head and tail are already touching
            return;
        }
        if x_delta != 0 {
            self.knots[knot_index].x += x_delta / x_delta.abs();
        }

        if y_delta != 0 {
            self.knots[knot_index].y += y_delta / y_delta.abs();
        }
    }

    fn execute_move(&mut self, dir: Direction, dist: u32) {
        for _i in 0..dist {
            self.move_head_one(dir);
            for j in 1..10 {
                self.tail_response(j);
            }
            self.tail_history.insert(self.knots[9]);
        }
    }
}

fn solve_puzzle(input_string: &String) -> u32 {
    let mut rope = Rope {
        knots: Default::default(),
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
    let expected_sample_output = 36;

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
