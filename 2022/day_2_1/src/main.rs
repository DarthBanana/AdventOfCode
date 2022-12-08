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
fn get_result(player_choice : Choice, opp_choice : Choice) -> RoundResult {
    match player_choice {
        Choice::Rock => match opp_choice {
            Choice::Rock => return RoundResult::Tie,
            Choice::Paper => return RoundResult::Lose,
            Choice::Scissors => return RoundResult::Win
        },
        Choice::Paper => match opp_choice {
            Choice::Rock => return RoundResult::Win,
            Choice::Paper => return RoundResult::Tie,
            Choice::Scissors => return RoundResult::Lose
        }, 
        Choice::Scissors => match opp_choice {
            Choice::Rock => return RoundResult::Lose,
            Choice::Paper => return RoundResult::Win,
            Choice::Scissors => return RoundResult::Tie
        }, 
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

fn get_my_choice(line_string: &str) -> Choice {
    match line_string.chars().nth(2).expect("INVALID_INPUT!") {
        'X' => return Choice::Rock,
        'Y' => return Choice::Paper,
        'Z' => return Choice::Scissors,
        _ => panic!("INVALID_SYNTAX"),
    }
}

fn solve_puzzle(input_string: &String) {
    let mut score = 0;
    for line in input_string.lines() {

        let my_choice = get_my_choice(&line);
        let opp_choice = get_opponent_choice(&line);
        let result = get_result(my_choice, opp_choice);
        //println!("{my_choice} {opp_choice} {result}");
        score += my_choice.score() + result.score();     
    }

    println!("Result : {score}");
}

fn main() {
    println!("Day 2 : Part 1!");    
    let test_input_string = std::fs::read_to_string(std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("sample.txt")).unwrap();
    let real_input_string = std::fs::read_to_string(std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("input.txt")).unwrap();

    println!("Sample:");
    solve_puzzle(&test_input_string);

    println!("Real:");
    solve_puzzle(&real_input_string);
}
