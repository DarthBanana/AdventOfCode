use std::collections::HashSet;

#[derive(Debug, Clone)]
struct Map {
    cubes: Vec<(i32, i32, i32)>,
    cube_map: HashSet<(i32, i32, i32)>,
}

impl Default for Map {
    fn default() -> Self {
        Map {
            cubes: Vec::new(),
            cube_map: HashSet::new(),
        }
    }
}

impl Map {
    fn init_from_string(&mut self, input_string: &String) {
        for line in input_string.lines() {
            let point = sscanf::sscanf!(line, "{},{},{}", i32, i32, i32).unwrap();
            self.cubes.push(point);
            self.cube_map.insert(point);
        }
    }
    fn count_sides_of_cube(&self, cube: &(i32, i32, i32)) -> u32 {
        let mut count = 0;
        let neighbors = vec![
            (cube.0 - 1, cube.1, cube.2),
            (cube.0 + 1, cube.1, cube.2),
            (cube.0, cube.1 - 1, cube.2),
            (cube.0, cube.1 + 1, cube.2),
            (cube.0, cube.1, cube.2 - 1),
            (cube.0, cube.1, cube.2 + 1),
        ];
        for neighbor in neighbors {
            if !self.cube_map.contains(&neighbor) {
                count += 1;
            }
        }
        count
    }

    fn count_all_sides(&self) -> u32 {
        let mut count = 0;
        for cube in self.cubes.iter() {
            count += self.count_sides_of_cube(cube);
        }
        count
    }
}

fn solve_puzzle(input_string: &String) -> u32 {
    let mut map: Map = Default::default();
    map.init_from_string(input_string);
    map.count_all_sides()
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 64;

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
