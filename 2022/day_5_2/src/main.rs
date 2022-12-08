// [D]
// [N] [C]
// [Z] [M] [P]
//  1   2   3

// [T] [V]                     [W]
// [V] [C] [P] [D]             [B]
// [J] [P] [R] [N] [B]         [Z]
// [W] [Q] [D] [M] [T]     [L] [T]
// [N] [J] [H] [B] [P] [T] [P] [L]
// [R] [D] [F] [P] [R] [P] [R] [S] [G]
// [M] [W] [J] [R] [V] [B] [J] [C] [S]
// [S] [B] [B] [F] [H] [C] [B] [N] [L]
//  1   2   3   4   5   6   7   8   9

use std::collections::VecDeque;

fn solve_puzzle(input_string: &String, stack_count: u32) {    
    let mut stacks: Vec<VecDeque<char>> = Vec::new();
    for _i in 0..stack_count {
        //let mut new_stack: VecDeque<char> = VecDeque::new();
        stacks.push(VecDeque::new());
    }
    for line in input_string.lines() {
        if line.contains('[') {            
            for stack_number in 0..stack_count {
                let new_crate = line
                    .chars()
                    .nth((stack_number * 4 + 1) as usize)
                    .expect("didn't get crate");
                if new_crate.is_alphabetic() {
                    //stacks[stack_number as usize].push_back(new_crate);
                    stacks
                        .get_mut(stack_number as usize)
                        .unwrap()
                        .push_back(new_crate);
                }
            }
        } else if line.contains("move") {
            let (count, source, dest) =
                sscanf::sscanf!(line, "move {} from {} to {}", usize, usize, usize)
                    .expect("FAILED TO PARSE LINE");
            let mut grabs = VecDeque::new();
            for _j in 0..count {

                let new_crate = stacks[source - 1].pop_front().expect("Couldn't pop");
                grabs.push_back(new_crate);
                
            }
            for _j in 0..count {
                stacks[dest - 1].push_front(grabs.pop_back().unwrap());
            }

        } else {
            println!("ignoring line");
        }
    }

    println!("{:?}", stacks);
    print!("Result : ");
    for st in &stacks {
        print!("{}", st.front().expect("uh oh"));
    }

    println!("");
}

fn main() {
    println!("Day 5 : Part 2!");
    let test_input_string = std::fs::read_to_string(
        std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("sample.txt"),
    )
    .unwrap();
    let real_input_string =
        std::fs::read_to_string(std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("input.txt"))
            .unwrap();

    println!("Sample:");
    solve_puzzle(&test_input_string, 3);

    println!("Real:");
    solve_puzzle(&real_input_string, 9);
}
