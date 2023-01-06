use std::cmp::{max, min};

struct Reindeer {
    name: String,
    speed: u32,
    fly_duration: u32,
    rest_duration: u32,
}

fn solve_puzzle(input_string: &String, duration: u32) -> u32 {
    let mut result = 0;
    let mut reindeer: Vec<Reindeer> = Vec::new();

    for line in input_string.lines() {
        let (name, speed, fly_duration, rest_duration) = sscanf::sscanf!(
            line,
            "{} can fly {} km/s for {} seconds, but then must rest for {} seconds.",
            String,
            u32,
            u32,
            u32
        )
        .unwrap();
        let new_reindeer = Reindeer {
            name,
            speed,
            fly_duration,
            rest_duration,
        };
        reindeer.push(new_reindeer);
    }

    for r in reindeer {
        //
        // first, get the cycle length
        //
        let cycle = r.fly_duration + r.rest_duration;
        let cycle_distance = r.fly_duration * r.speed;

        let mut distance = 0;
        //
        // How many complete cycles were there
        //
        let cycle_count = duration / cycle;

        distance += cycle_count * cycle_distance;

        //
        // Now check the remainder
        //
        let remainder = min(r.fly_duration, duration % cycle);
        distance += remainder * r.speed;
        result = max(result, distance);
    }

    result
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 1120;

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
    let result = solve_puzzle(&test_input_string, 1000);
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
    let result = solve_puzzle(&real_input_string, 2503);
    println!("Real Result : {}", result);
}
