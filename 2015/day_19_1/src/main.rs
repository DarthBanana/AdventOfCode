use std::default;

struct Puzzle {
    replacements: Vec<(String, String)>,
    starting_string: String,
}

impl Puzzle {
    fn create_from_string(input_string: &String) -> Self {
        let mut puzzle = Self {
            replacements: Vec::new(),
            starting_string: Default::default(),
        };
        for line in input_string.lines() {
            if line.contains("=>") {
                let (from, to) = sscanf::sscanf!(line, "{} => {}", String, String).unwrap();
                puzzle.replacements.push((from, to));
            } else if line.len() > 4 {
                puzzle.starting_string = line.to_string();
            }
        }
        puzzle
    }

    fn calibrate(&self) -> usize {
        let mut derived_molecules: Vec<String> = Vec::new();
        for (from, to) in self.replacements.iter() {
            let original = self.starting_string.as_str();
            for (start, part) in original.match_indices(from) {
                let mut new_string = String::new();
                new_string.push_str(&original.get(0..start).unwrap());
                new_string.push_str(to.as_str());
                new_string.push_str(
                    self.starting_string
                        .get(start + part.len()..original.len())
                        .unwrap(),
                );
                derived_molecules.push(new_string);
            }
        }
        derived_molecules.sort();
        derived_molecules.dedup();
        derived_molecules.len()
    }
}

fn solve_puzzle(input_string: &String) -> usize {
    let puzzle = Puzzle::create_from_string(input_string);

    puzzle.calibrate()
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 7;

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
