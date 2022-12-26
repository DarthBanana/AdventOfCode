use std::collections::VecDeque;

fn dec_to_snafu(dec: i64) -> String {
    let mut result = String::new();
    let mut remainder = dec;
    let mut snafu: VecDeque<i64> = VecDeque::new();

    let mut mul = 1;
    let mut count = 1;
    while dec / mul > 4 {
        mul *= 5;
        count += 1;
    }

    for _i in 0..count {
        snafu.push_back(remainder / mul);
        remainder = remainder % mul;
        mul = mul / 5;
    }
    while snafu.len() > 0 {
        let mut d = snafu.pop_back().unwrap();

        while d > 2 {
            if snafu.len() > 0 {
                let front = snafu.back_mut().unwrap();
                *front = *front + 1;
                d -= 5;
            }
        }
        let c = match d {
            2 => '2',
            1 => '1',
            0 => '0',
            -1 => '-',
            -2 => '=',
            _ => panic!("Invalid digit"),
        };
        result.insert(0, c);
    }
    result
}

fn snafu_to_dec(snafu: &str) -> i64 {
    let mut mul = 1;
    let mut result = 0;
    for c in snafu.chars().rev() {
        let val = match c {
            '2' => 2,
            '1' => 1,
            '0' => 0,
            '-' => -1,
            '=' => -2,
            _ => panic!("invalid input char"),
        };
        result += val * mul;
        mul *= 5;
    }
    result
}
fn solve_puzzle(input_string: &String) -> String {
    let mut result = 0;

    for line in input_string.lines() {
        result += snafu_to_dec(line);
    }
    dec_to_snafu(result)
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = "2=-1=0";

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
