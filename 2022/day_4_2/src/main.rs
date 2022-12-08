fn solve_puzzle(input_string: &String) {
    let mut score = 0;

    for line in input_string.lines() {
        let parsed =
            sscanf::sscanf!(line, "{}-{},{}-{}", u32, u32, u32, u32).expect("FAILED TO PARSE LINE");
        if parsed.1 < parsed.2 {
        } else if parsed.3 < parsed.0 {
        } else {
            score += 1;
        }
    }
    println!("Result : {score}");
}

fn main() {
    println!("Day 4 : Part 2!");
    let test_input_string = std::fs::read_to_string(
        std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("sample.txt"),
    )
    .unwrap();
    let real_input_string =
        std::fs::read_to_string(std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("input.txt"))
            .unwrap();

    println!("Sample:");
    solve_puzzle(&test_input_string);

    println!("Real:");
    solve_puzzle(&real_input_string);
}
