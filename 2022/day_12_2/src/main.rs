use std::collections::HashMap;

#[derive(Default, Debug)]
struct Map {
    grid: HashMap<(i32, i32), i32>,
    paths: HashMap<(i32, i32), u32>,
    starts: Vec<(i32, i32)>,
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
                if c == 'S' || c == 'a' {
                    self.starts.push(current_position);
                    self.grid.insert(current_position, get_alt_from_char('a'));
                } else if c == 'E' {
                    self.end = current_position;
                    self.grid.insert(current_position, get_alt_from_char('z'));
                } else {
                    self.grid.insert(current_position, get_alt_from_char(c));
                }
                current_position.0 += 1;
            }
            current_position.1 += 1;
        }
    }

    fn get_list_of_previous_steps(&self, position: (i32, i32)) -> Vec<(i32, i32)> {
        let mut steps: Vec<(i32, i32)> = Vec::new();
        let cur = self.grid.get(&position).unwrap();
        let moves = [(-1, 0), (1, 0), (0, 1), (0, -1)];

        for m in moves {
            let next_coord = (position.0 + m.0, position.1 + m.1);
            if self.paths.contains_key(&next_coord) {
                continue;
            }
            match self.grid.get(&next_coord) {
                Some(loc) => {
                    if *loc >= *cur - 1 {
                        steps.push(next_coord);
                    }
                }
                None => (),
            }
        }
        steps
    }

    fn find_shortest_path_to_end(&mut self) {
        let mut temp: Vec<(i32, i32)> = Vec::new();
        let mut all_next_steps: Vec<(i32, i32)> = Vec::new();
        //
        // Start at the end
        //

        all_next_steps.push(self.end);
        let mut depth = 0;
        loop {
            temp.clear();
            if all_next_steps.is_empty() {
                break;
            }
            all_next_steps.sort();
            all_next_steps.dedup();
            for pos in all_next_steps.iter() {
                self.paths.insert(*pos, depth);
                let mut prev = self.get_list_of_previous_steps(*pos);
                temp.append(&mut prev);
            }
            all_next_steps.clear();
            all_next_steps.append(&mut temp);
            depth += 1;
        }
    }

    fn get_shortest_path_to_end(&mut self) -> u32 {
        let mut paths: Vec<u32> = Vec::new();
        let starts = self.starts.clone();
        self.find_shortest_path_to_end();

        for start in starts {
            println!("Starting with ({},{})", start.0, start.1);
            if start == (0, 30) {
                println!("here");
            }

            let res = self.paths.get(&start);
            if res.is_some() {
                paths.push(*res.unwrap());
            }
        }
        paths.sort();
        paths[0]
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
    let expected_sample_output = 29;

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
