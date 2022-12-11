use std::{cell::RefCell, collections::VecDeque};
#[derive(Debug, Copy, Clone)]
enum Operation {
    Add(i64),
    Multiply(i64),
    SelfAdd,
    SelfMultiply,
}

impl Operation {
    fn operate(&self, worry: i64) -> i64 {
        match self {
            Operation::Add(val) => worry + val,
            Operation::Multiply(val) => worry * val,
            Operation::SelfAdd => worry + worry,
            Operation::SelfMultiply => worry * worry,
        }
    }
}

#[derive(Debug, Copy, Clone)]
struct Test {
    value: i64,
    test_true: usize,
    test_false: usize,
}

impl Test {
    fn run_test(&self, worry: i64) -> usize {
        if worry % self.value == 0 {
            // println!("    Current worry level is divisible by {}", self.value);
            self.test_true
        } else {
            // println!("    Current worry level is not divisible by {}", self.value);
            self.test_false
        }
    }
}
#[derive(Debug)]
struct Monkey {
    id: usize,
    items: RefCell<VecDeque<i64>>,
    op: Operation,
    test: Test,
}
impl Default for Monkey {
    fn default() -> Self {
        Monkey {
            id: 0,
            items: RefCell::new(VecDeque::new()),
            op: Operation::Add(0),
            test: Test {
                value: 0,
                test_true: 0,
                test_false: 0,
            },
        }
    }
}

impl Monkey {
    fn throw_stuff(&self) -> Vec<(usize, i64)> {
        // println!("Monkey {}:", self.id);

        let mut throws: Vec<(usize, i64)> = Vec::new();
        for mut item in self.items.borrow_mut().drain(..) {
            // println!("  Monkey inspects an item with a worry level of {}", item);
            item = self.op.operate(item);
            // println!("    Worry level is {:?} to {}", self.op, item);

            item = item / 3;
            // println!("    Monkey gets bored with item.  Worry level is divided by 3 to {}", item);
            let target = self.test.run_test(item);
            // println!("    Item with worry level {} is thrown to Monkey {}", item, target);
            throws.push((target, item));
        }
        throws
    }
    fn catch(&self, item: i64) {
        self.items.borrow_mut().push_back(item);
    }

    fn init(&mut self, input_file: &str) {
        let mut lines = input_file.lines();
        let mut line = lines.next().unwrap();
        // println!("{}", line);
        self.id = sscanf::sscanf!(line, "Monkey {}:", usize).unwrap();
        line = lines.next().unwrap().trim();
        //
        // Next line is Starting items
        //
        line = line.strip_prefix("Starting items: ").unwrap().trim();
        for substr in line.split(',') {
            let val = substr.trim();
            // println!("item: {}", val);
            let item: i64 = sscanf::sscanf!(val, "{}", i64).unwrap();
            self.items.borrow_mut().push_back(item);
        }

        //
        // Next is the operation
        //
        line = lines.next().unwrap().trim();

        let ans = sscanf::sscanf!(line, "Operation: new = old {} {}", char, str).unwrap();
        self.op = match ans {
            ('*', "old") => Operation::SelfMultiply,
            ('*', x) => Operation::Multiply(x.parse().unwrap()),
            ('+', "old") => Operation::SelfAdd,
            ('+', x) => Operation::Add(x.parse().unwrap()),
            _ => panic!("oh no"),
        };

        //
        // Next line is the test:
        //
        line = lines.next().unwrap().trim();
        self.test.value = sscanf::sscanf!(line, "Test: divisible by {}", i64).unwrap();
        line = lines.next().unwrap().trim();
        self.test.test_true = sscanf::sscanf!(line, "If true: throw to monkey {}", usize).unwrap();
        line = lines.next().unwrap().trim();
        self.test.test_false =
            sscanf::sscanf!(line, "If false: throw to monkey {}", usize).unwrap();
    }
}

#[derive(Debug, Default)]
struct Troop {
    monkeys: Vec<Monkey>,
    counts: Vec<u32>,
    round: u32,
    items_inspected: u32,
}
impl Troop {
    fn build_troop(&mut self, input_string: &String) {
        for monkey_input in input_string.split("\r\n\r\n") {
            let mut monkey: Monkey = Default::default();
            monkey.init(monkey_input);

            self.monkeys.push(monkey);
            self.counts.push(0);
        }
        self.round = 0;
        self.items_inspected = 0;
    }

    fn run_round(&mut self) {
        self.round += 1;
        for monkey in self.monkeys.iter() {
            let throws = monkey.throw_stuff();

            for (target, item) in throws {
                self.items_inspected += 1;
                self.counts[monkey.id] += 1;
                self.monkeys[target].catch(item);
            }
        }
    }
}

fn solve_puzzle(input_string: &String) -> u32 {
    let mut troop: Troop = Default::default();
    troop.build_troop(input_string);
    for _i in 0..20 {
        troop.run_round();
    }

    troop.counts.sort();
    troop.counts.reverse();
    troop.counts.iter().take(2).product()
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 10605;

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
