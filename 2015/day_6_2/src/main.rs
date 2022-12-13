enum Operation {
    On,
    Off,
    Toggle,
}

struct Parameters {
    start: (usize, usize),
    end: (usize, usize),
    op: Operation,
}

fn get_paramaters(input_string: &str) -> Parameters {
    let mut op: Operation = Operation::On;
    let mut start = (0, 0);
    let mut end = (0, 0);

    if input_string.contains("toggle") {
        (start.0, start.1, end.0, end.1) = sscanf::sscanf!(
            input_string,
            "toggle {},{} through {},{}",
            usize,
            usize,
            usize,
            usize
        )
        .unwrap();
        op = Operation::Toggle;
    } else if input_string.contains("on") {
        op = Operation::On;
        (start.0, start.1, end.0, end.1) = sscanf::sscanf!(
            input_string,
            "turn on {},{} through {},{}",
            usize,
            usize,
            usize,
            usize
        )
        .unwrap();
    } else {
        op = Operation::Off;
        (start.0, start.1, end.0, end.1) = sscanf::sscanf!(
            input_string,
            "turn off {},{} through {},{}",
            usize,
            usize,
            usize,
            usize
        )
        .unwrap();
    }
    let result = Parameters { start, end, op };
    result
}

fn solve_puzzle(input_string: &String) -> u32 {
    let mut lights: Vec<Vec<u32>> = vec![vec![0; 1000]; 1000];
    println!("Starting");
    for line in input_string.lines() {
        println!("{}", line);
        let params = get_paramaters(&line);
        for y in params.start.1..=params.end.1 {
            for x in params.start.0..=params.end.0 {
                lights[x][y] = match params.op {
                    Operation::On => lights[x][y] + 1,
                    Operation::Off => lights[x][y].saturating_sub(1),
                    Operation::Toggle => lights[x][y] + 2,
                }
            }
        }
    }

    let mut result = 0;
    for y in 0..1000 {
        for x in 0..1000 {
            result += lights[x][y];
        }
    }
    result
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 2000001;

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
