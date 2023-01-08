use regex::Regex;

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
            .replacements
            .sort_by(|a, b| b.1.len().cmp(&a.1.len()));
        puzzle
    }

    fn count_steps_to_make_molecule(&self) -> u64 {
        //
        // Ok, so every replacement grows the string.  This means that the depth is bounded
        //
        // Each operation on an element creates a pair of new elements, the second of which may be
        // a nested list of elements.  The groups are defined by Rn and Ar, with Y separating each element in the group.  So think
        // of Rn Y Ar as ( , )
        // We can either go from A => BC, A=> B(C), A => B(C,D), OR A=> B(C,D,E)
        //
        //
        // We know that a group is created in one step, adding at least the Rn and Ar.  If there are Ys in there, there is an extra element created at the same
        // time for each Y.
        //
        // So we can count all of the elements except for Rn, Ar, and Y.
        // Then for every Y, we deduct one from the element count because those elements were created "for free"
        //
        // That leaves us with only BCs and B(C) which are created in the same number of steps.  So we can ignore the Rn and Ars and just take the
        // remaining element count and subtract 1 (since we started with "e") and that is the answer

        //
        // First count the Ys
        //
        let re = Regex::new(r"[[:upper:]][[:lower:]]*").unwrap();
        let mut element_count = 0;
        let mut y_count = 0;
        for element in re.find_iter(&self.starting_string) {
            match element.as_str() {
                "Rn" => (),
                "Ar" => (),
                "Y" => y_count += 1,
                _ => element_count += 1,
            };
        }
        println!("Elements: {}, Ys: {}", element_count, y_count);
        element_count - y_count - 1
    }
}

fn solve_puzzle(input_string: &String) -> u64 {
    let puzzle = Puzzle::create_from_string(input_string);

    puzzle.count_steps_to_make_molecule()
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 5;

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
