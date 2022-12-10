fn solve_puzzle(input_string: &String) -> i32 {
    let mut result = 0;

    for c in input_string.chars() {
        match c {
            '(' => result += 1,
            ')' => result -= 1,
            _ => panic!("bad input"),
        };        
    }

    result
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    //let expected_sample_output = ;

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
    let mut lines = test_input_string.lines();
    
    loop
    {
        let line = match lines.next() {
            Some(x) => x,
            None => break,
        };
        
        let expected_sample_output = dbg!(sscanf::sscanf!(line, "{}", i32).unwrap());
        let result = solve_puzzle(&lines.next().unwrap().to_string());
        println!("{}", result);
        if result != expected_sample_output {
            println!("Wrong Answer!!!!! {}", result);
            return;
        }
    }
    //
    // Read in the real input
    //
    let real_input_string =
        std::fs::read_to_string(std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("input.txt"))
            .unwrap();


    //
    // Solve for the real input, only in the case that the result
    // for the sample input was correct
    //
    println!("Testing Real Data:");
    let result = solve_puzzle(&real_input_string);
    println!("Real Result : {}", result);
}