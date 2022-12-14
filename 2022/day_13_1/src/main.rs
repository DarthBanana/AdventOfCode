use std::cmp::Ordering;

use fancy_regex::Regex;
#[derive(Debug)]
enum Symbol {
    List(Vec<Symbol>),
    Integer(u32),
}

#[derive(Debug)]
struct Pair {
    left: Symbol,
    right: Symbol,
}

fn parse_integer(input: &str) -> u32 {
    input.parse().unwrap()
}

fn parse_list(input: &str) -> (Symbol, &str) {
    let mut list: Vec<Symbol> = Vec::new();
    let mut rest_of_input = input;
    let integer_regex = Regex::new(r"^\d+").unwrap();

    while !rest_of_input.is_empty() {
        let c = rest_of_input.chars().nth(0).unwrap();
        match c {
            '[' => {
                let res = parse_list(&rest_of_input[1..]);
                list.push(res.0);
                rest_of_input = res.1;
            }
            ',' => {
                rest_of_input = &rest_of_input[1..];
            }
            ']' => {
                return (Symbol::List(list), &rest_of_input[1..]);
            }
            _ => {
                let integer_res = integer_regex.find(rest_of_input).unwrap().unwrap();
                let num = parse_integer(integer_res.as_str());
                list.push(Symbol::Integer(num));
                rest_of_input = &rest_of_input[integer_res.end()..];
            }
        }
    }
    (Symbol::List(list), rest_of_input)
}

fn parse_line(input: &str) -> Symbol {
    //
    // The line is always a list
    //

    let substr = input.strip_prefix('[').unwrap();
    let res = parse_list(substr);
    res.0

    //println!("input: {}, list: {}", input, list_str);
}

fn make_list_from_number(num: u32) -> Vec<Symbol> {
    let res = vec![Symbol::Integer(num)];
    res
}
fn are_symbols_ordered(left: &Symbol, right: &Symbol) -> Ordering {
    match left {
        Symbol::List(l) => match right {
            Symbol::List(r) => {
                return are_lists_ordered(l, r);
            }
            Symbol::Integer(r) => {
                return are_lists_ordered(l, &make_list_from_number(*r));
            }
        },
        Symbol::Integer(l) => match right {
            Symbol::List(r) => {
                return are_lists_ordered(&make_list_from_number(*l), r);
            }
            Symbol::Integer(r) => {
                if l < r {
                    return Ordering::Less;
                } else if l == r {
                    return Ordering::Equal;
                } else {
                    return Ordering::Greater;
                }
            }
        },
    }
}

fn are_lists_ordered(left: &Vec<Symbol>, right: &Vec<Symbol>) -> Ordering {
    let left_len = left.len();

    for i in 0..left_len {
        if i >= right.len() {
            return Ordering::Greater;
        }
        let res = are_symbols_ordered(&left[i], &right[i]);
        match res {
            Ordering::Less => return res,
            Ordering::Greater => return res,
            Ordering::Equal => continue,
        }
    }
    if left.len() > right.len() {
        return Ordering::Greater;
    } else if left.len() < right.len() {
        return Ordering::Less;
    } else {
        return Ordering::Equal;
    }
}

fn parse_input(input_string: &String) -> Vec<Pair> {
    let mut pairs: Vec<Pair> = Vec::new();
    let mut right_line = false;

    let mut left = Symbol::Integer(0);
    let mut right: Symbol;

    for line in input_string.lines() {
        if line.contains('[') {
            let res = parse_line(line);
            if right_line {
                right = res;
                pairs.push(Pair {
                    left: left,
                    right: right,
                });
                left = Symbol::Integer(0);
            } else {
                left = res;
            }
            right_line = !right_line;
        }
    }
    pairs
}

fn solve_puzzle(input_string: &String) -> u32 {
    let mut result = 0;
    let mut index = 0;
    let pairs = parse_input(input_string);
    for pair in pairs {
        index += 1;
        let res = are_symbols_ordered(&pair.left, &pair.right);
        match res {
            Ordering::Less => {
                println!("{} is valid", index);
                result += index;
            }
            Ordering::Greater => (),
            Ordering::Equal => (),
        }
    }
    result
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 13;

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
