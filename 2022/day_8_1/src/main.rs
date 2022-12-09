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

    fn is_visible(&self, row: usize, col: usize) -> bool {
        let tree_height = self.get_tree(row, col);

        let mut visible = true;

        //
        // Check from the left
        //
        for i in 0..col {
            if self.get_tree(row, i) >= tree_height {
                visible = false;
                break;
            }
        }
        if visible {
            return true;
        }
        //
        // Check from the right
        //
        visible = true;
        for i in (col + 1)..self.cols {
            if self.get_tree(row, i) >= tree_height {
                visible = false;
                break;
            }
        }
        if visible {
            return true;
        }

        //
        // Check from the top
        //
        visible = true;
        for i in 0..row {
            if self.get_tree(i, col) >= tree_height {
                visible = false;
                break;
            }
        }
        if visible {
            return true;
        }

        //
        // Check from the bottom
        //
        visible = true;
        for i in row + 1..self.rows {
            if self.get_tree(i, col) >= tree_height {
                visible = false;
                break;
            }
        }
        if visible {
            return true;
        }
        return false;
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
            if map.is_visible(row, col) {
                result += 1;
            }
        }
    }
    result
}

fn main() {
    let expected_sample_output = 21;

    let (day, part) = sscanf::sscanf!(env!("CARGO_PKG_NAME"), "day_{}_{}", u32, u32).unwrap();
    println!("Day {} : Part {}!", day, part);

    let test_input_string = std::fs::read_to_string(
        std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("sample.txt"),
    )
    .unwrap();

    let real_input_string =
        std::fs::read_to_string(std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("input.txt"))
            .unwrap();

    println!("Testing Sample Data:");
    let result = solve_puzzle(&test_input_string);
    println!("Sample Result : {}", result);

    if result != expected_sample_output {
        println!("Wrong Answer!!!!! {}", result);
    } else {
        println!("Testing Real Data:");
        let result = solve_puzzle(&real_input_string);
        println!("Real Result : {}", result);
    }
}
