use std::fmt::Display;

#[derive(Debug, Copy, Clone)]
enum Choice {
    Rock,
    Paper,
    Scissors
}
impl Choice {
    fn score(&self) -> u32 {
        match self {
            Choice::Rock => 1,
            Choice::Paper => 2,
            Choice::Scissors => 3,
        }
    }
}
impl Display for Choice {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {        
        std::fmt::Debug::fmt(&self, f)
    }
}

#[derive(Debug, Copy, Clone)]
enum RoundResult {
    Win,
    Tie,
    Lose
}
impl RoundResult {
    fn score(&self) -> u32 {
        match self {
            RoundResult::Win => 6,
            RoundResult::Tie => 3,
            RoundResult::Lose => 0,
        }
    }
}
impl Display for RoundResult {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {        
        std::fmt::Debug::fmt(&self, f)
    }
}
fn get_result(line_string: &str) -> RoundResult {
    match line_string.chars().nth(2).expect("INVALID_INPUT!") {
        'X' => return RoundResult::Lose,
        'Y' => return RoundResult::Tie,
        'Z' => return RoundResult::Win,
        _ => panic!("INVALID_SYNTAX"),
    }
}
fn get_opponent_choice(line_string: &str) -> Choice {
    match line_string.chars().nth(0).expect("INVALID_INPUT") {
        'A' => return Choice::Rock,
        'B' => return Choice::Paper,
        'C' => return Choice::Scissors,
        _ => panic!("INVALID_SYNTAX"),
    }
}

fn get_my_choice(opp_choice : Choice, result : RoundResult) -> Choice {

    match opp_choice {
        Choice::Rock => match result {
            RoundResult::Win => Choice::Paper,
            RoundResult::Tie => Choice::Rock,
            RoundResult::Lose => Choice::Scissors,
        },
        Choice::Paper => match result {
            RoundResult::Win => Choice::Scissors,
            RoundResult::Tie => Choice::Paper,
            RoundResult::Lose => Choice::Rock,
        }, 
        Choice::Scissors => match result {
            RoundResult::Win => Choice::Rock,
            RoundResult::Tie => Choice::Scissors,
            RoundResult::Lose => Choice::Paper,
        }, 

    }
}

fn solve_puzzle(input_string: &String) {
    let mut score = 0;
    for line in input_string.lines() {

        
        let opp_choice = get_opponent_choice(&line);
        let result = get_result(&line);
        let my_choice = get_my_choice(opp_choice, result);
        //println!("{my_choice} {opp_choice} {result}");
        score += my_choice.score() + result.score();     
    }

    println!("Result : {score}");
}

fn main() {
    println!("Day 2 : Part 2!");    
    let test_input_string = std::fs::read_to_string(std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("sample.txt")).unwrap();
    let real_input_string = std::fs::read_to_string(std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("input.txt")).unwrap();

    println!("Sample:");
    solve_puzzle(&test_input_string);

    println!("Real:");
    solve_puzzle(&real_input_string);    
}
