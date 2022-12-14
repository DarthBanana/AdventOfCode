fn look_and_say(input: String) -> String {
    let mut output = String::new();
    let mut current_char = '0';
    let mut current_count = 0;
    for c in input.chars() {
        if current_count > 0 {
            if c == current_char {
                current_count += 1;
            } else {
                output.push_str(format!("{}", current_count).as_str());
                output.push(current_char);
                current_count = 1;
                current_char = c;
            }
        } else {
            current_count = 1;
            current_char = c;
        }
    }
    output.push_str(format!("{}", current_count).as_str());
    output.push(current_char);
    output
}
fn solve_puzzle(input_string: &String, iterations: u32) -> usize {
    let mut output = input_string.clone();

    for _i in 0..iterations {
        output = look_and_say(output);
    }

    //println!("{}", output);

    output.len()
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 6;

    //
    // Print the specific puzzle info
    //
    let (day, part) = sscanf::sscanf!(env!("CARGO_PKG_NAME"), "day_{}_{}", u32, u32).unwrap();
    println!("Day {} : Part {}!", day, part);

    //
    // Read in the real input
    //

    //
    // Solve for the sample input
    //
    println!("Testing Sample Data:");
    let result = solve_puzzle(&"1".to_string(), 5);
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
    let result = solve_puzzle(&"1321131112".to_string(), 50);
    println!("Real Result : {}", result);
}
