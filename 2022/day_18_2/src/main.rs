use std::{
    cmp::{max, min},
    collections::HashMap,
};

#[derive(PartialEq, Eq)]
enum Contents {
    Steam,
    Lava,
    Perimeter,
}
#[derive()]
struct Map {
    cubes: Vec<(i32, i32, i32)>,
    cube_map: HashMap<(i32, i32, i32), Contents>,
    min_x: i32,
    max_x: i32,
    min_y: i32,
    max_y: i32,
    min_z: i32,
    max_z: i32,
}

impl Default for Map {
    fn default() -> Self {
        Map {
            cubes: Vec::new(),
            cube_map: HashMap::new(),
            min_x: i32::MAX,
            max_x: i32::MIN,
            min_y: i32::MAX,
            max_y: i32::MIN,
            min_z: i32::MAX,
            max_z: i32::MIN,
        }
    }
}

impl Map {
    fn init_from_string(&mut self, input_string: &String) {
        for line in input_string.lines() {
            let point = sscanf::sscanf!(line, "{},{},{}", i32, i32, i32).unwrap();
            self.cubes.push(point);
            self.cube_map.insert(point, Contents::Lava);
            self.min_x = min(self.min_x, point.0);
            self.min_y = min(self.min_y, point.1);
            self.min_z = min(self.min_z, point.2);
            self.max_x = max(self.max_x, point.0);
            self.max_y = max(self.max_y, point.1);
            self.max_z = max(self.max_z, point.2);
        }
    }

    fn create_perimeter(&mut self) {
        for x in (self.min_x - 2)..=(self.max_x + 2) {
            for y in (self.min_y - 2)..=(self.max_y + 2) {
                self.cube_map
                    .insert((x, y, self.min_z - 2), Contents::Perimeter);
                self.cube_map
                    .insert((x, y, self.max_z + 2), Contents::Perimeter);
            }
        }
        for x in (self.min_x - 2)..=(self.max_x + 2) {
            for z in (self.min_z - 2)..=(self.max_z + 2) {
                self.cube_map
                    .insert((x, self.min_y - 2, z), Contents::Perimeter);
                self.cube_map
                    .insert((x, self.max_y + 2, z), Contents::Perimeter);
            }
        }
        for y in (self.min_y - 2)..=(self.max_y + 2) {
            for z in (self.min_z - 2)..=(self.max_z + 2) {
                self.cube_map
                    .insert((self.min_x - 2, y, z), Contents::Perimeter);
                self.cube_map
                    .insert((self.max_x + 2, y, z), Contents::Perimeter);
            }
        }
    }

    fn simulate_steam(&mut self) {
        let mut open_steam: Vec<(i32, i32, i32)> = Vec::new();
        //
        // first create the perimeter
        //
        self.create_perimeter();

        //
        // Now, create the first layer of steam
        //
        for x in (self.min_x - 1)..=(self.max_x + 1) {
            for y in (self.min_y - 1)..=(self.max_y + 1) {
                let p1 = (x, y, self.min_z - 1);
                let p2 = (x, y, self.max_z + 1);
                self.cube_map.insert(p1, Contents::Steam);
                self.cube_map.insert(p2, Contents::Steam);
                open_steam.push(p1);
                open_steam.push(p2);
            }
        }
        for x in (self.min_x - 1)..=(self.max_x + 1) {
            for z in (self.min_z - 1)..=(self.max_z + 1) {
                let p1 = (x, self.min_y - 1, z);
                let p2 = (x, self.max_y + 1, z);
                self.cube_map.insert(p1, Contents::Steam);
                self.cube_map.insert(p2, Contents::Steam);
                open_steam.push(p1);
                open_steam.push(p2);
            }
        }
        for y in (self.min_y - 1)..=(self.max_y + 1) {
            for z in (self.min_z - 1)..=(self.max_z + 1) {
                let p1 = (self.min_x - 1, y, z);
                let p2 = (self.max_x + 1, y, z);
                self.cube_map.insert(p1, Contents::Steam);
                self.cube_map.insert(p2, Contents::Steam);
                open_steam.push(p1);
                open_steam.push(p2);
            }
        }

        //
        // Now, let the steam expand
        //
        while !open_steam.is_empty() {
            let mut candidates: Vec<(i32, i32, i32)> = open_steam.drain(..).collect();
            for steam in candidates {
                let neighbors = vec![
                    (steam.0 - 1, steam.1, steam.2),
                    (steam.0 + 1, steam.1, steam.2),
                    (steam.0, steam.1 - 1, steam.2),
                    (steam.0, steam.1 + 1, steam.2),
                    (steam.0, steam.1, steam.2 - 1),
                    (steam.0, steam.1, steam.2 + 1),
                ];
                for neighbor in neighbors {
                    if !self.cube_map.contains_key(&neighbor) {
                        self.cube_map.insert(neighbor, Contents::Steam);
                        open_steam.push(neighbor);
                    }
                }
            }
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
            if let Some(contents) = self.cube_map.get(&neighbor) {
                if *contents == Contents::Steam {
                    count += 1;
                }
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
    map.simulate_steam();
    map.count_all_sides()
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 58;

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
