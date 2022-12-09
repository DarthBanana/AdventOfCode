struct Map {
    trees: String,
    rows: usize,
    cols: usize,
}

impl Map {
    fn get_tree(&self, row: usize, col: usize) -> u32 {
        let line = self.trees.lines().nth(row).unwrap();
        let c = line.chars().nth(col).unwrap();
        c.to_digit(10).unwrap()
    }

    fn get_scenic_score(&self, row: usize, col: usize) -> u32 {
        let mut up_score = 0;
        let mut down_score = 0;
        let mut left_score = 0;
        let mut right_score = 0;
        let tree_height = self.get_tree(row, col);

        //
        // Get up score
        //
        for i in 0..row {
            up_score += 1;
            if self.get_tree((row - 1) - i, col) >= tree_height {
                break;
            }
        }

        //
        // Get down score
        //
        for i in (row + 1)..self.rows {
            down_score += 1;
            if self.get_tree(i, col) >= tree_height {
                break;
            }
        }

        //
        // Get left score
        //
        for i in 0..col {
            left_score += 1;
            if self.get_tree(row, (col - 1) - i) >= tree_height {
                break;
            }
        }

        //
        // Get right score
        //
        for i in (col + 1)..self.cols {
            right_score += 1;
            if self.get_tree(row, i) >= tree_height {
                break;
            }
        }

        let score = up_score * down_score * left_score * right_score;
        return score;
    }
}

fn solve_puzzle(input_string: &String) -> u32 {
    let mut result = 0;
    let rows = input_string.lines().count();
    let cols = input_string.lines().nth(0).unwrap().len();
    let map = Map {
        trees: input_string.clone(),
        rows: rows,
        cols: cols,
    };

    for row in 0..rows {
        for col in 0..cols {
            let score = map.get_scenic_score(row, col);
            if score > result {
                result = score;
            }
        }
    }
    result
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 8;

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
