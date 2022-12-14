use std::{
    cmp::{max, min},
    collections::HashMap,
};

enum Solid {
    Rock,
    Sand,
}

struct Cave {
    map: HashMap<(i32, i32), Solid>,
    min_x: i32,
    min_y: i32,
    max_x: i32,
    max_y: i32,
}
impl Default for Cave {
    fn default() -> Self {
        Cave {
            map: HashMap::new(),
            min_x: 500,
            min_y: 0,
            max_x: 500,
            max_y: 0,
        }
    }
}
impl Cave {
    fn init_map_from_string(&mut self, input_string: &String) {
        for line in input_string.lines() {
            let mut last_point: Option<(i32, i32)> = None;
            for coordstr in line.split(" -> ") {
                let coord = sscanf::sscanf!(coordstr, "{},{}", i32, i32).unwrap();

                match last_point {
                    Some(start) => {
                        let min_x = min(start.0, coord.0);
                        let min_y = min(start.1, coord.1);
                        let max_x = max(start.0, coord.0);
                        let max_y = max(start.1, coord.1);

                        if min_x < self.min_x {
                            self.min_x = min_x;
                        }
                        if max_x > self.max_x {
                            self.max_x = max_x;
                        }
                        if max_y > self.max_y {
                            self.max_y = max_y;
                        }
                        if min_y < self.min_y {
                            self.min_y = min_y;
                        }
                        for x in min_x..=max_x {
                            for y in min_y..=max_y {
                                self.map.insert((x, y), Solid::Rock);
                            }
                        }
                    }
                    None => (),
                }

                last_point = Some(coord);
            }
        }
    }

    fn drop_sand(&mut self, coord: (i32, i32)) -> bool {
        if coord.0 < self.min_x
            || coord.0 > self.max_x
            || coord.1 < self.min_y
            || coord.1 > self.max_y
        {
            return false;
        }

        let down = (coord.0, coord.1 + 1);
        let down_left = (coord.0 - 1, coord.1 + 1);
        let down_right = (coord.0 + 1, coord.1 + 1);

        if !self.map.contains_key(&down) {
            return self.drop_sand(down);
        }
        if !self.map.contains_key(&down_left) {
            return self.drop_sand(down_left);
        }
        if !self.map.contains_key(&down_right) {
            return self.drop_sand(down_right);
        }
        self.map.insert(coord, Solid::Sand);
        return true;
    }

    fn draw_map(&self) {
        for y in self.min_y..=self.max_y {
            for x in self.min_x..=self.max_x {
                match self.map.get(&(x, y)) {
                    Some(x) => match x {
                        Solid::Rock => print!("#"),
                        Solid::Sand => print!("o"),
                    },
                    None => print!("."),
                }
                print!(" ");
            }
            print!("\n");
        }
    }
}
fn solve_puzzle(input_string: &String) -> u32 {
    let mut cave: Cave = Default::default();
    cave.init_map_from_string(input_string);

    let mut result = 0;

    while cave.drop_sand((500, 0)) {
        result += 1;
    }

    cave.draw_map();

    result
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 24;

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
