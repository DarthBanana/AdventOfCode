use std::collections::HashSet;

#[derive(Eq, Hash, PartialEq, Copy, Clone)]
struct Position {
    x: i32,
    y: i32,
}

fn solve_puzzle(input_string: &String) -> usize {
    let mut map: HashSet<Position> = HashSet::new();
    let mut current_position = Position { x: 0, y: 0 };

    map.insert(current_position);
    for line in input_string.lines() {
        for c in line.chars() {
            match c {
                '^' => current_position.y += 1,
                '>' => current_position.x += 1,
                'v' => current_position.y -= 1,
                '<' => current_position.x -= 1,
                _ => panic!("Invalid Input"),
            };
            map.insert(current_position);
        }
    }
    map.len()
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 2;

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
