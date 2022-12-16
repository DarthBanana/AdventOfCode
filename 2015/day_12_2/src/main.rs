use serde_json::{Map, Value};

fn count_no_red(value: &Value) -> i64 {
    match value {
        Value::Number(n) => n.as_i64().unwrap(),

        Value::Array(arr) => arr.iter().map(count_no_red).sum(),
        Value::Object(obj) => {
            let mut sum = 0;
            for value in obj.values() {
                if let Value::String(value) = value {
                    if value == "red" {
                        return 0;
                    }
                }
                sum += count_no_red(value);
            }
            sum
        }
        _ => 0,
    }
}

fn solve_puzzle(input_string: &String) -> i64 {
    let mut result = 0;

    for line in input_string.lines() {
        println!("{}", line);
        let mut thingy: serde_json::Value = serde_json::from_str(line.trim()).unwrap();
        result += count_no_red(&thingy);
    }

    result
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 18;

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
