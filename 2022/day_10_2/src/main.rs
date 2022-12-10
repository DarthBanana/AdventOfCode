use std::cell::RefCell;

struct CPU {
    cycle: i32,
    x: i32,
    col: i32,
    history: RefCell<Vec<(i32, i32)>>,
    pixels: RefCell<Vec<bool>>,
}
impl Default for CPU {
    fn default() -> Self {
        CPU {
            col: 39,
            cycle: 0,
            x: 1,
            history: RefCell::new(Vec::new()),
            pixels: RefCell::new(Vec::new()),
        }
    }
}

impl CPU {
    fn tick(&mut self) {
        self.cycle += 1;
        self.col = (self.col + 1) % 40;
        if self.col == 0 {
            print!("\n");
        }
        if (self.x == self.col) || ((self.x + 1) == self.col) || ((self.x - 1) == self.col) {
            self.pixels.borrow_mut().push(true);

            print!("#");
        } else {
            self.pixels.borrow_mut().push(false);
            print!(".");
        }
        self.history.borrow_mut().push((self.cycle, self.x));
    }

    fn noop(&mut self) {
        self.tick();
    }
    fn addx(&mut self, v: i32) {
        self.tick();
        self.x += v;
        self.tick();
    }
    fn run_program(&mut self, input_string: &String) {
        self.tick();
        for line in input_string.lines() {
            if line.contains("noop") {
                self.noop();
            } else {
                let val = sscanf::sscanf!(line, "addx {}", i32).unwrap();
                self.addx(val);
            }
        }
    }
    fn calc_signal_strengths(&mut self) -> Vec<i32> {
        let mut strengths = Vec::new();
        let mut next_cycle = 20;
        for (c, x) in self.history.borrow().iter() {
            if *c == next_cycle {
                let sig_strength = c * x;
                next_cycle += 40;
                strengths.push(sig_strength);
            }
        }
        return strengths;
    }

    fn draw_screen(&mut self) {
        let mut col = 0;
        for p in self.pixels.borrow().iter() {
            if *p {
                print!("#");
            } else {
                print!(".");
            }
            col += 1;
            if (col % 40) == 0 {
                print!("\n");
            }
        }
    }
}

fn solve_puzzle(input_string: &String) -> i32 {
    let mut cpu: CPU = Default::default();
    cpu.run_program(input_string);

    //cpu.draw_screen();
    let mut result = 0;

    result
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 0;

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
