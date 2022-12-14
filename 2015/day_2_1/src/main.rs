fn solve_puzzle(input_string: &String) -> u32 {
    let mut result = 0;

    for line in input_string.lines() {
        let (length, width, height) = sscanf::sscanf!(line, "{}x{}x{}", u32, u32, u32).unwrap();
        let mut faces = vec![length * width, length * height, width * height];
        faces.sort();

        let area = faces[0] * 3 + faces[1] * 2 + faces[2] * 2;
        result += area;
    }

    result
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 58 + 43;

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
