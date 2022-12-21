use std::{cell::RefCell, collections::HashMap};

#[derive(Clone)]
enum Operation {
    Add(String, String),
    Sub(String, String),
    Mult(String, String),
    Div(String, String),
    Num(i64),
}

#[derive()]
struct Monkey {
    _name: String,
    operation: Operation,
}

#[derive()]
struct Troop {
    monkeys: HashMap<String, Monkey>,
    known_values: RefCell<HashMap<String, i64>>,
}

impl Default for Troop {
    fn default() -> Self {
        Troop {
            monkeys: HashMap::new(),
            known_values: RefCell::new(HashMap::new()),
        }
    }
}

impl Troop {
    fn init_from_string(&mut self, input_string: &String) {
        for line in input_string.lines() {
            if line.contains('+') {
                let (name, mon1, mon2) =
                    sscanf::sscanf!(line, "{}: {} + {}", String, String, String).unwrap();
                let monkey = Monkey {
                    _name: name.clone(),
                    operation: Operation::Add(mon1, mon2),
                };
                self.monkeys.insert(name, monkey);
            } else if line.contains('-') {
                let (name, mon1, mon2) =
                    sscanf::sscanf!(line, "{}: {} - {}", String, String, String).unwrap();
                let monkey = Monkey {
                    _name: name.clone(),
                    operation: Operation::Sub(mon1, mon2),
                };
                self.monkeys.insert(name, monkey);
            } else if line.contains('/') {
                let (name, mon1, mon2) =
                    sscanf::sscanf!(line, "{}: {} / {}", String, String, String).unwrap();
                let monkey = Monkey {
                    _name: name.clone(),
                    operation: Operation::Div(mon1, mon2),
                };
                self.monkeys.insert(name, monkey);
            } else if line.contains('*') {
                let (name, mon1, mon2) =
                    sscanf::sscanf!(line, "{}: {} * {}", String, String, String).unwrap();
                let monkey = Monkey {
                    _name: name.clone(),
                    operation: Operation::Mult(mon1, mon2),
                };
                self.monkeys.insert(name, monkey);
            } else {
                let (name, val) = sscanf::sscanf!(line, "{}: {}", String, i64).unwrap();
                let monkey = Monkey {
                    _name: name.clone(),
                    operation: Operation::Num(val),
                };
                self.monkeys.insert(name.clone(), monkey);
                self.known_values.borrow_mut().insert(name, val);
            }
        }
    }

    fn find_number(&self, name: &String) -> i64 {
        match self.known_values.borrow().get(name) {
            Some(v) => return *v,
            None => (),
        }

        let monkey = self.monkeys.get(name).unwrap();
        let value = match &monkey.operation {
            Operation::Add(m1, m2) => self.find_number(&m1) + self.find_number(&m2),
            Operation::Sub(m1, m2) => self.find_number(&m1) - self.find_number(&m2),
            Operation::Mult(m1, m2) => self.find_number(&m1) * self.find_number(&m2),
            Operation::Div(m1, m2) => self.find_number(&m1) / self.find_number(&m2),
            Operation::Num(v) => *v,
        };

        self.known_values.borrow_mut().insert(name.clone(), value);
        return value;
    }
}

fn solve_puzzle(input_string: &String) -> i64 {
    let mut troop: Troop = Default::default();

    troop.init_from_string(input_string);
    troop.find_number(&"root".to_string())
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 152;

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
