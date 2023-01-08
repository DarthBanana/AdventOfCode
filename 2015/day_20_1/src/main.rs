fn count_presents(house: u64) -> u64 {
    let mut presents = 0;
    //println!("{}", house);
    let mut divs = divisors::get_divisors(house);
    //
    // Address bug in divisors.
    //

    if house != 2 {
        //assert!(!divs.contains(&house));
        divs.push(house);
    }

    divs.dedup();

    //
    // 1 isn't included
    //
    presents += 10;

    for d in divs {
        //println!("  {}", d);
        presents += 10 * d;
    }
    println!("house: {}, presents: {}", house, presents);
    presents
}
fn solve_puzzle(target: u64) -> u64 {
    let mut result = 0;
    let max_house = target / 10;
    for i in 1..max_house {
        if count_presents(i) >= target {
            return i;
        }
    }
    0
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 8;

    //
    // Print the specific puzzle info
    //
    let (day, part) = sscanf::sscanf!(env!("CARGO_PKG_NAME"), "day_{}_{}", u32, u32).unwrap();
    println!("Day {} : Part {}!", day, part);

    //
    // Solve for the sample input
    //
    println!("Testing Sample Data:");
    let result = solve_puzzle(140);
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
    let result = solve_puzzle(29000000);
    println!("Real Result : {}", result);
}
