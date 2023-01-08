#[derive(Default)]
struct Puzzle {
    containers: Vec<u32>,
    count: u32,
}
impl Puzzle {
    fn init_from_string(&mut self, input_string: &String) {
        for line in input_string.lines() {
            let val = sscanf::sscanf!(line, "{}", u32).unwrap();
            self.containers.push(val);
        }
    }
    fn fill_next_container(&mut self, index: usize, volume_left: u32) {
        if volume_left == 0 {
            self.count += 1;
            return;
        }
        if index == self.containers.len() {
            return;
        }
        //
        // Try filling this one
        //
        if volume_left >= self.containers[index] {
            self.fill_next_container(index + 1, volume_left - self.containers[index]);
        }
        //
        // Try not filling this one
        //
        self.fill_next_container(index + 1, volume_left);
    }
}

fn solve_puzzle(input_string: &String, volume: u32) -> u32 {
    let mut puzzle: Puzzle = Default::default();

    puzzle.init_from_string(input_string);
    puzzle.fill_next_container(0, volume);

    puzzle.count
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 4;

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
    let result = solve_puzzle(&test_input_string, 25);
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
    let result = solve_puzzle(&real_input_string, 150);
    println!("Real Result : {}", result);
}
