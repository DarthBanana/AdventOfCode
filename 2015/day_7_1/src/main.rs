use fancy_regex::Regex;
use std::{cell::RefCell, collections::HashMap};

#[derive(Debug)]
enum Input {
    Wire(String),
    Value(u16),
}
#[derive(Debug)]
enum Source {
    Direct(Input),

    AND(Input, Input),
    OR(Input, Input),
    LSHIFT(Input, u16),
    RSHIFT(Input, u16),
    NOT(Input),
}
#[derive(Debug)]
struct Circuit {
    inputs: HashMap<String, Source>,
    outputs: RefCell<HashMap<String, u16>>,
}

impl Default for Circuit {
    fn default() -> Self {
        Circuit {
            inputs: HashMap::new(),
            outputs: RefCell::new(HashMap::new()),
        }
    }
}

fn get_input(input_field: &str) -> Input {
    let value_input_re = Regex::new(r"^\d").unwrap();
    if value_input_re.is_match(input_field).unwrap() {
        Input::Value(input_field.parse().unwrap())
    } else {
        Input::Wire(input_field.to_string())
    }
}
impl Circuit {
    fn build_circuit(&mut self, input_string: &String) {
        let mut inputs: HashMap<String, Source> = HashMap::new();
        for line in input_string.lines() {
            if line.contains("AND") {
                let (in1, in2, out) =
                    sscanf::sscanf!(line, "{} AND {} -> {}", str, str, str).unwrap();
                inputs.insert(out.to_string(), Source::AND(get_input(in1), get_input(in2)));
            } else if line.contains("OR") {
                let (in1, in2, out) =
                    sscanf::sscanf!(line, "{} OR {} -> {}", str, str, str).unwrap();
                inputs.insert(out.to_string(), Source::OR(get_input(in1), get_input(in2)));
            } else if line.contains("LSHIFT") {
                let (in1, in2, out) =
                    sscanf::sscanf!(line, "{} LSHIFT {} -> {}", str, u16, str).unwrap();
                inputs.insert(out.to_string(), Source::LSHIFT(get_input(in1), in2));
            } else if line.contains("RSHIFT") {
                let (in1, in2, out) =
                    sscanf::sscanf!(line, "{} RSHIFT {} -> {}", str, u16, str).unwrap();
                inputs.insert(out.to_string(), Source::RSHIFT(get_input(in1), in2));
            } else if line.contains("NOT") {
                let (in1, out) = sscanf::sscanf!(line, "NOT {} -> {}", str, str).unwrap();
                inputs.insert(out.to_string(), Source::NOT(get_input(in1)));
            } else {
                let (in1, out) = sscanf::sscanf!(line, "{} -> {}", str, str).unwrap();
                inputs.insert(out.to_string(), Source::Direct(get_input(in1)));
            }
        }
        self.inputs = inputs;
    }

    fn get_input_value(&self, input: &Input) -> u16 {
        match input {
            Input::Wire(x) => self.get_wire_value(&x),
            Input::Value(x) => *x,
        }
    }
    fn get_wire_value(&self, wire_name: &String) -> u16 {
        let name = wire_name.as_str();

        match self.outputs.borrow().get(&name.to_string()) {
            Some(x) => return *x,
            None => (),
        }
        let source = self.inputs.get(&wire_name.clone()).unwrap();
        let value = match source {
            Source::Direct(in1) => self.get_input_value(in1),
            Source::AND(in1, in2) => self.get_input_value(in1) & self.get_input_value(in2),
            Source::OR(in1, in2) => self.get_input_value(in1) | self.get_input_value(in2),
            Source::LSHIFT(in1, in2) => self.get_input_value(in1) << in2,
            Source::RSHIFT(in1, in2) => self.get_input_value(in1) >> in2,
            Source::NOT(in1) => !self.get_input_value(in1),
        };
        self.outputs.borrow_mut().insert(name.to_string(), value);
        value
    }
}

fn solve_puzzle(input_string: &String, wire: &String) -> u16 {
    let mut circuit: Circuit = Default::default();
    circuit.build_circuit(input_string);

    /*for wire in circuit.inputs.keys() {
        println!("{}: {}", wire, circuit.get_wire_value(wire));
    }*/

    circuit.get_wire_value(wire)
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 114;

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
    let result = solve_puzzle(&test_input_string, &"g".to_string());
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
    let result = solve_puzzle(&real_input_string, &"a".to_string());
    println!("Real Result : {}", result);
}
