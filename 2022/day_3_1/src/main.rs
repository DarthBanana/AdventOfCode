fn calc_score(letter : char) -> u32 {
    assert!(letter.is_alphabetic());

    if letter.is_lowercase() {
        return (letter as u32) - ('a' as u32) + 1;
    } else if letter.is_uppercase() {
        return (letter as u32) - ('A' as u32) + 27;
    } else {
        panic!("Character isn't a letter");
    }
}

fn solve_puzzle(input_string: &String) {
    let mut score = 0;
    for line in input_string.lines() {
        let rucksack = line.split_at(line.len()/2);
        println!("{} - {}", rucksack.0, rucksack.1);
        for c in rucksack.0.chars() {
            if rucksack.1.contains(c) {
                println!("{}", c);
                score += calc_score(c);
                break;
            }
        }
    }

    println!("Result : {score}");
}

fn main() {
    println!("Day 3 : Part 1!");    
    let test_input_string = std::fs::read_to_string(std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("sample.txt")).unwrap();
    let real_input_string = std::fs::read_to_string(std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("input.txt")).unwrap();

    println!("Sample:");
    solve_puzzle(&test_input_string);

    println!("Real:");
    solve_puzzle(&real_input_string);
}
