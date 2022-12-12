use std::collections::HashMap;

#[derive(Default, Debug, Copy, Clone)]
struct Location {
    alt: i32,
    shortest_path: Option<u32>,
}
#[derive(Default, Debug)]
struct Map {
    grid: HashMap<(i32, i32), Location>,
    start: (i32, i32),
    end: (i32, i32),
}

fn get_alt_from_char(c: char) -> i32 {
    (c as i32) - ('a' as i32)
}
impl Map {
    fn init_from_string(&mut self, input_string: &String) {
        let mut current_position = (0, 0);
        for line in input_string.lines() {
            current_position.0 = 0;
            for c in line.chars() {
                if c == 'S' {
                    self.start = current_position;
                    self.grid.insert(
                        current_position,
                        Location {
                            alt: get_alt_from_char('a'),
                            shortest_path: None,
                        },
                    );
                } else if c == 'E' {
                    self.end = current_position;
                    self.grid.insert(
                        current_position,
                        Location {
                            alt: get_alt_from_char('z'),
                            shortest_path: None,
                        },
                    );
                } else {
                    self.grid.insert(
                        current_position,
                        Location {
                            alt: get_alt_from_char(c),
                            shortest_path: None,
                        },
                    );
                }
                current_position.0 += 1;
            }
            current_position.1 += 1;
        }
    }

    fn get_list_of_next_steps(&self, position: (i32, i32)) -> Vec<(i32, i32)> {
        let mut steps: Vec<(i32, i32)> = Vec::new();
        let cur = self.grid.get(&position).unwrap();
        let moves = [(-1, 0), (1, 0), (0, 1), (0, -1)];

        for m in moves {
            let next_coord = (position.0 + m.0, position.1 + m.1);
            match self.grid.get(&next_coord) {
                Some(loc) => {
                    if loc.alt > (cur.alt + 1) {
                        ();
                    } else {
                        steps.push(next_coord);
                    }
                }
                None => (),
            }
        }
        steps
    }

    fn find_shortest_path_to_end(&mut self, position: (i32, i32), path_length: u32) {
        let loc = self.grid.get(&position).unwrap();
        if (loc.shortest_path == None) || (loc.shortest_path.unwrap() > path_length) {
            let new_loc = Location {
                alt: loc.alt,
                shortest_path: Some(path_length),
            };
            self.grid.insert(position, new_loc);
        } else {
            return;
        }
        if position == self.end {
            return;
        }
        let moves = self.get_list_of_next_steps(position);
        for m in moves {
            self.find_shortest_path_to_end(m, path_length + 1);
        }
    }

    fn get_shortest_path_to_end(&mut self) -> u32 {
        self.find_shortest_path_to_end(self.start, 0);
        self.grid.get(&self.end).unwrap().shortest_path.unwrap()
    }
}
fn solve_puzzle(input_string: &String) -> u32 {
    let mut map: Map = Default::default();

    map.init_from_string(input_string);
    map.get_shortest_path_to_end()
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 31;

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
