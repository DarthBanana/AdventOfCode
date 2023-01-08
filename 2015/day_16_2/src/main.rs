use std::collections::HashMap;

struct AuntSue {
    id: u32,
    compounds: Vec<(String, u32)>,
}

impl AuntSue {
    fn new(input_string: &str) -> Self {
        let (id, pname0, pval0, pname1, pval1, pname2, pval2) = sscanf::sscanf!(
            input_string,
            "Sue {}: {}: {}, {}: {}, {}: {}",
            u32,
            String,
            u32,
            String,
            u32,
            String,
            u32
        )
        .unwrap();
        Self {
            id,
            compounds: vec![(pname0, pval0), (pname1, pval1), (pname2, pval2)],
        }
    }
}
fn solve_puzzle(input_string: &String) -> u32 {
    let mut auntsues: Vec<AuntSue> = Vec::new();
    let mut detected_compounds: HashMap<String, u32> = HashMap::new();
    let mut found = false;

    detected_compounds.insert("children".to_string(), 3);
    detected_compounds.insert("cats".to_string(), 7);
    detected_compounds.insert("samoyeds".to_string(), 2);
    detected_compounds.insert("pomeranians".to_string(), 3);
    detected_compounds.insert("akitas".to_string(), 0);
    detected_compounds.insert("vizslas".to_string(), 0);
    detected_compounds.insert("goldfish".to_string(), 5);
    detected_compounds.insert("trees".to_string(), 3);
    detected_compounds.insert("cars".to_string(), 2);
    detected_compounds.insert("perfumes".to_string(), 1);
    for line in input_string.lines() {
        let sue = AuntSue::new(line);
        auntsues.push(sue);
    }

    for sue in auntsues {
        for (name, value) in sue.compounds {
            found = true;
            let res = *detected_compounds.get(&name).unwrap();
            let cmp = match name.as_str() {
                "cats" | "trees" => value > res,
                "pomeranians" | "goldfish" => value < res,
                _ => value == res,
            };
            if !cmp {
                found = false;
                break;
            }
        }
        if found {
            return sue.id;
        }
    }
    0
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 10;

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
