fn calc_score(letter: char) -> u32 {
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
    let mut elves = input_string.lines();
    loop {
        let elf1 = match elves.next() {
            Some(val) => val,
            None => break,
        };
        let elf2 = elves.next().expect("PARSE_ERROR!");
        let elf3 = elves.next().expect("PARSE_ERROR!");

        for c in elf1.chars() {
            if elf2.contains(c) && elf3.contains(c) {
                //println!("{}", c);
                score += calc_score(c);
                break;
            }
        }
    }

    println!("Result : {score}");
}

fn main() {
    println!("Day 3 : Part 2!");
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
