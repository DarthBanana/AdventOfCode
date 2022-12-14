use std::{
    cmp::max,
    collections::{HashMap, VecDeque},
};

#[derive(Debug, Default)]
struct World {
    city_ordinals: HashMap<String, usize>,
    city_distances: HashMap<(usize, usize), u32>,
    next_ordinal: usize,
    longest_path: u32,
}

impl World {
    fn get_ordinal(&mut self, city: &str) -> usize {
        let ord = match self.city_ordinals.get(city) {
            Some(x) => *x,
            None => {
                self.city_ordinals
                    .insert(city.to_string(), self.next_ordinal);
                self.next_ordinal += 1;
                self.next_ordinal - 1
            }
        };
        ord
    }
    fn init_from_string(&mut self, input_string: &String) {
        self.longest_path = u32::MIN;
        for line in input_string.lines() {
            let (city1, city2, dist) =
                sscanf::sscanf!(line, "{} to {} = {}", str, str, u32).unwrap();
            let ord1 = self.get_ordinal(city1);
            let ord2 = self.get_ordinal(city2);
            self.city_distances.insert((ord1, ord2), dist);
            self.city_distances.insert((ord2, ord1), dist);
        }
    }
    fn next_hop(&mut self, cur: usize, avail: &mut VecDeque<usize>, dist: u32) {
        //
        // Are we at the end?
        //
        if avail.is_empty() {
            self.longest_path = max(self.longest_path, dist);
        }
        let count = avail.len();
        for _i in 0..count {
            let city = avail.pop_front().unwrap();
            let hop = self.city_distances.get(&(cur, city)).unwrap();
            self.next_hop(city, avail, dist + *hop);
            avail.push_back(city);
        }
    }
    fn follow_paths(&mut self) {
        let mut avail: VecDeque<usize> = VecDeque::new();

        for i in 0..self.next_ordinal {
            avail.push_back(i);
        }

        for _i in 0..self.next_ordinal {
            let city = avail.pop_front().unwrap();
            self.next_hop(city, &mut avail, 0);
            avail.push_back(city);
        }
    }
}
fn solve_puzzle(input_string: &String) -> u32 {
    let mut world: World = Default::default();
    world.init_from_string(input_string);
    world.follow_paths();
    world.longest_path
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 982;

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
