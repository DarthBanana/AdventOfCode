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

    fn find_known_numbers(&self, name: &String) -> Option<i64> {
        if name == "humn" {
            return None;
        }

        match self.known_values.borrow().get(name) {
            Some(v) => return Some(*v),
            None => (),
        }

        let monkey = self.monkeys.get(name).unwrap();
        let value = match &monkey.operation {
            Operation::Add(m1, m2) => {
                let input1 = self.find_known_numbers(&m1);
                let input2 = self.find_known_numbers(&m2);
                match input1 {
                    Some(v1) => match input2 {
                        Some(v2) => Some(v1 + v2),
                        None => None,
                    },
                    None => None,
                }
            }

            Operation::Sub(m1, m2) => {
                let input1 = self.find_known_numbers(&m1);
                let input2 = self.find_known_numbers(&m2);
                match input1 {
                    Some(v1) => match input2 {
                        Some(v2) => Some(v1 - v2),
                        None => None,
                    },
                    None => None,
                }
            }
            Operation::Mult(m1, m2) => {
                let input1 = self.find_known_numbers(&m1);
                let input2 = self.find_known_numbers(&m2);
                match input1 {
                    Some(v1) => match input2 {
                        Some(v2) => Some(v1 * v2),
                        None => None,
                    },
                    None => None,
                }
            }
            Operation::Div(m1, m2) => {
                let input1 = self.find_known_numbers(&m1);
                let input2 = self.find_known_numbers(&m2);
                match input1 {
                    Some(v1) => match input2 {
                        Some(v2) => Some(v1 / v2),
                        None => None,
                    },
                    None => None,
                }
            }
            Operation::Num(v) => Some(*v),
        };

        if value.is_some() {
            self.known_values
                .borrow_mut()
                .insert(name.clone(), value.unwrap());
        }
        return value;
    }

    fn find_unknown_numbers(&self, name: &String, value: i64) {
        self.known_values.borrow_mut().insert(name.clone(), value);

        if name == "humn" {
            return;
        }
        let monkey = self.monkeys.get(name).unwrap();
        let (next, expected) = match &monkey.operation {
            Operation::Add(m1, m2) => {
                let map = self.known_values.borrow();
                let input1 = map.get(m1).clone();
                let input2 = map.get(m2).clone();

                if input2.is_none() {
                    (m2, value - input1.unwrap())
                } else {
                    (m1, value - input2.unwrap())
                }
            }

            Operation::Sub(m1, m2) => {
                let map = self.known_values.borrow();
                let input1 = map.get(m1).clone();
                let input2 = map.get(m2).clone();

                if input2.is_none() {
                    (m2, input1.unwrap() - value)
                } else {
                    (m1, value + input2.unwrap())
                }
            }
            Operation::Mult(m1, m2) => {
                let map = self.known_values.borrow();
                let input1 = map.get(m1).clone();
                let input2 = map.get(m2).clone();

                if input2.is_none() {
                    (m2, value / input1.unwrap())
                } else {
                    (m1, value / input2.unwrap())
                }
            }

            Operation::Div(m1, m2) => {
                let map = self.known_values.borrow();
                let input1 = map.get(m1).clone();
                let input2 = map.get(m2).clone();

                if input2.is_none() {
                    (m2, input1.unwrap() / value)
                } else {
                    (m1, value * input2.unwrap())
                }
            }

            Operation::Num(v) => panic!("not here!"),
        };
        self.find_unknown_numbers(next, expected)
    }
}

fn solve_puzzle(input_string: &String) -> i64 {
    let mut troop: Troop = Default::default();
    troop.init_from_string(input_string);
    let root = troop.monkeys.get(&"root".to_string()).unwrap();
    let (input1, input2) = match &root.operation {
        Operation::Add(i1, i2) => (i1, i2),
        Operation::Sub(i1, i2) => (i1, i2),
        Operation::Mult(i1, i2) => (i1, i2),
        Operation::Div(i1, i2) => (i1, i2),
        Operation::Num(_) => panic!("root shouldn't be a number"),
    };

    let res1 = troop.find_known_numbers(&input1);
    let res2 = troop.find_known_numbers(&input2);
    if res1.is_none() {
        println!("{}", res2.unwrap());
        troop.find_unknown_numbers(&input1, res2.unwrap());
    } else if res2.is_none() {
        println!("{}", res1.unwrap());
        troop.find_unknown_numbers(&input2, res1.unwrap());
    }
    let result = *troop
        .known_values
        .borrow()
        .get(&"humn".to_string())
        .unwrap();
    result
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 301;

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
