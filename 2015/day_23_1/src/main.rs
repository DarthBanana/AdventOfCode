use std::collections::HashMap;

#[derive(Debug)]
enum Instruction {
    Hlf(usize),
    Tpl(usize),
    Inc(usize),
    Jmp(i32),
    Jie(usize, i32),
    Jio(usize, i32),
}
struct Computer {
    register_map: HashMap<String, usize>,
    registers: Vec<u32>,
    program: Vec<Instruction>,
}

impl Computer {
    fn new() -> Self {
        Self {
            register_map: HashMap::from([("a".to_string(), 0), ("b".to_string(), 1)]),
            registers: vec![0, 0],
            program: Vec::new(),
        }
    }

    fn load_program(&mut self, input_string: &String) {
        for l in input_string.lines() {
            let line = l.replace("+", "");
            if line.contains("hlf") {
                let r = sscanf::sscanf!(line, "hlf {}", String).unwrap();
                self.program
                    .push(Instruction::Hlf(*self.register_map.get(&r).unwrap()));
            } else if line.contains("tpl") {
                let r = sscanf::sscanf!(line, "tpl {}", String).unwrap();
                self.program
                    .push(Instruction::Tpl(*self.register_map.get(&r).unwrap()));
            } else if line.contains("inc") {
                let r = sscanf::sscanf!(line, "inc {}", String).unwrap();
                self.program
                    .push(Instruction::Inc(*self.register_map.get(&r).unwrap()));
            } else if line.contains("jmp") {
                let offset = sscanf::sscanf!(line, "jmp {}", i32).unwrap();
                self.program.push(Instruction::Jmp(offset));
            } else if line.contains("jie") {
                let (r, offset) = sscanf::sscanf!(line, "jie {}, {}", String, i32).unwrap();
                let reg = *self.register_map.get(&r).unwrap();
                self.program.push(Instruction::Jie(reg, offset));
            } else if line.contains("jio") {
                let (r, offset) = sscanf::sscanf!(line, "jio {}, {}", String, i32).unwrap();
                let reg = *self.register_map.get(&r).unwrap();
                self.program.push(Instruction::Jio(reg, offset));
            } else {
                panic!();
            }
        }
    }

    fn run_program(&mut self) {
        let mut ip = 0;

        while ip < self.program.len() {
            let inst = &self.program[ip];
            println!(
                "{}: ({},{}) {:?}",
                ip, self.registers[0], self.registers[1], inst
            );
            match *inst {
                Instruction::Hlf(r) => {
                    self.registers[r] = self.registers[r] / 2;
                    ip += 1;
                }
                Instruction::Tpl(r) => {
                    self.registers[r] = self.registers[r] * 3;
                    ip += 1;
                }
                Instruction::Inc(r) => {
                    self.registers[r] += 1;
                    ip += 1;
                }
                Instruction::Jmp(o) => {
                    ip = ((ip as i32) + o) as usize;
                }
                Instruction::Jie(r, o) => {
                    if self.registers[r] & 1 == 0 {
                        ip = ((ip as i32) + o) as usize;
                    } else {
                        ip += 1;
                    }
                }
                Instruction::Jio(r, o) => {
                    if self.registers[r] == 1 {
                        ip = ((ip as i32) + o) as usize;
                    } else {
                        ip += 1;
                    }
                }
            }
        }
    }
}

fn solve_puzzle(input_string: &String) -> (u32, u32) {
    let mut result = 0;
    let mut computer = Computer::new();

    computer.load_program(input_string);
    computer.run_program();

    (computer.registers[0], computer.registers[1])
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = (2, 0);

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
    println!("Sample Result : ({}, {})", result.0, result.1);

    //
    // Check if the sample input matches the expected result
    //
    if result != expected_sample_output {
        println!("Wrong Answer!!!!!  ({}, {})", result.0, result.1);
        return;
    }

    //
    // Solve for the real input, only in the case that the result
    // for the sample input was correct
    //
    println!("Testing Real Data:");
    let result = solve_puzzle(&real_input_string);
    println!("Real Result :  ({}, {})", result.0, result.1);
}
