use std::cmp::Ordering;

#[derive(Default)]
struct Puzzle {
    packages: Vec<u32>,
    solutions: Vec<Vec<u32>>,
    total_weight: u32,
    fewest_packages: usize,
}
fn get_quantum_entanglement(list: &Vec<u32>) -> u64 {
    let mut result = 1;
    for p in list {
        result *= *p as u64;
    }
    result
}

fn compare_lists(a: &Vec<u32>, b: &Vec<u32>) -> Ordering {
    if a.len() < b.len() {
        Ordering::Less
    } else if a.len() > b.len() {
        Ordering::Greater
    } else {
        let q_a = get_quantum_entanglement(a);
        let q_b = get_quantum_entanglement(b);
        q_a.cmp(&q_b)
    }
}
impl Puzzle {
    fn new(input_string: &String) -> Self {
        let mut puzzle: Puzzle = Default::default();
        puzzle.fewest_packages = usize::MAX;
        for line in input_string.lines() {
            let p = sscanf::sscanf!(line, "{}", u32).unwrap();
            puzzle.total_weight += p;
            puzzle.packages.push(p);
        }
        puzzle.packages.sort();
        puzzle.packages.reverse();
        puzzle
    }

    //
    // I currently assume that the solutions are all collections that add up to 1/3 of the total weight.  I think
    // it may be possible that there are such solutions where it isn't possible to make 2 more collections that add up
    // to the same 1/3 value.  I did get the correct answer, though.
    //
    fn find_fewest_packages_to_target(
        &mut self,
        target: u32,
        starting_index: usize,
        in_the_bag: &mut Vec<u32>,
    ) {
        if in_the_bag.len() >= self.fewest_packages {
            return;
        }
        for i in starting_index..self.packages.len() {
            let p = self.packages[i];
            if p > target {
                continue;
            }
            in_the_bag.push(p);
            if p == target {
                self.solutions.push(in_the_bag.clone());
                self.fewest_packages = in_the_bag.len();
            } else {
                self.find_fewest_packages_to_target(target - p, i + 1, in_the_bag)
            }
            in_the_bag.pop();
        }
    }

    fn solve(&mut self) -> u64 {
        self.find_fewest_packages_to_target(self.total_weight / 4, 0, &mut Vec::new());

        self.solutions.sort_by(|a, b| compare_lists(a, b));

        get_quantum_entanglement(&self.solutions[0])
    }
}

fn solve_puzzle(input_string: &String) -> u64 {
    let mut puzzle = Puzzle::new(input_string);

    puzzle.solve()
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 44;

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
    // Real answer is greater than 9279270607
    //
    println!("Testing Real Data:");
    let result = solve_puzzle(&real_input_string);
    println!("Real Result : {}", result);
}
