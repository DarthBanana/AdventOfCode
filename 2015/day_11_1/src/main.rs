use fancy_regex::Regex;
fn find_sequence(pass: &[char]) -> bool {
    let mut seq_count = 0;
    let mut last_char = 'a';
    for c in pass {
        if seq_count > 0 {
            if *c as u8 == (last_char as u8 + 1) {
                seq_count += 1;
                if seq_count > 2 {
                    return true;
                }
            } else {
                seq_count = 1;
            }
        } else {
            seq_count = 1;
        }
        last_char = *c;
    }
    return false;
}

fn is_valid(pass: &[char]) -> bool {
    let pass_str = String::from_iter(pass);
    let pairs_re = Regex::new(r"([a-z])(\1)").unwrap();
    let banned_letters_re = Regex::new(r"[i+o+l]").unwrap();
    let res = pairs_re.find_iter(&pass_str.as_str());
    if res.count() < 2 {
        return false;
    }
    if banned_letters_re.is_match(&pass_str.as_str()).unwrap() {
        return false;
    }
    return find_sequence(pass);
}

fn increment(pass: &mut [char]) {
    let mut index = pass.len() - 1;
    loop {
        let mut inc = 1;
        match pass[index] {
            'h' | 'n' | 'k' => inc = 2,
            'z' => {
                pass[index] = 'a';
                index -= 1;
                continue;
            }
            _ => (),
        };
        pass[index] = (pass[index] as u8 + inc) as char;
        break;
    }
}

fn solve_puzzle(input_string: &String) -> String {
    let blah: Vec<char> = input_string.chars().collect();
    let mut pass: [char; 8] = blah.try_into().unwrap();

    while !is_valid(&pass) {
        increment(&mut pass);
    }

    let result: String = pass.iter().collect();
    return result;
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = "abcdffaa";

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
    let result = solve_puzzle(&"abcdefgh".to_string());
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
    let result = solve_puzzle(&"vzbxxzaa".to_string());
    println!("Real Result : {}", result);
}
