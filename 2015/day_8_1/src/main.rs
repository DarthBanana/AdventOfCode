use fancy_regex::Regex;

fn solve_puzzle(input_string: &String) -> usize {
    let mut result = 0;
    let slash_escape = Regex::new(r"[\\]{2}").unwrap();
    let quote_escape = Regex::new(r#"[\\]["]"#).unwrap();
    let hex_escape = Regex::new(r"[\\][x][[:xdigit:]]{2}").unwrap();
    for line in input_string.lines() {
        let trim_string = line.trim();
        let size_in_code = trim_string.len();

        let trim_string = trim_string
            .strip_prefix(r#"""#)
            .unwrap()
            .strip_suffix(r#"""#)
            .unwrap();
        let short_string = slash_escape.replace_all(trim_string, "X");
        let short_string2 = quote_escape.replace_all(&short_string, "%");
        let short_string3 = hex_escape.replace_all(&short_string2, "_");

        let size_in_memory = short_string3.len();
        result += size_in_code - size_in_memory;
        println!("{}, {} - {}", size_in_code, size_in_memory, line);
    }

    result
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 12;

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
