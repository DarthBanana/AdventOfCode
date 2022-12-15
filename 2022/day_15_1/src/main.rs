use std::{
    cmp::{max, min},
    collections::HashSet,
};

struct Sensor {
    coord: (i32, i32),
    closest_beacon_dist: i32,
}
struct Cave {
    sensors: Vec<Sensor>,
    sensormap: HashSet<(i32, i32)>,
    beacons: HashSet<(i32, i32)>,
    min_x: i32,
    min_y: i32,
    max_x: i32,
    max_y: i32,
}
impl Default for Cave {
    fn default() -> Self {
        Cave {
            sensors: Vec::new(),
            beacons: HashSet::new(),
            sensormap: HashSet::new(),
            min_x: i32::MAX,
            min_y: i32::MAX,
            max_x: i32::MIN,
            max_y: i32::MIN,
        }
    }
}
fn calc_dist(point1: (i32, i32), point2: (i32, i32)) -> i32 {
    (point1.0 - point2.0).abs() + (point1.1 - point2.1).abs()
}
impl Cave {
    fn init_from_string(&mut self, input_string: &String) {
        for line in input_string.lines() {
            let (sx, sy, bx, by) = sscanf::sscanf!(
                line,
                "Sensor at x={}, y={}: closest beacon is at x={}, y={}",
                i32,
                i32,
                i32,
                i32
            )
            .unwrap();
            let dist = calc_dist((sx, sy), (bx, by));
            self.sensors.push(Sensor {
                coord: (sx, sy),
                closest_beacon_dist: dist,
            });
            self.beacons.insert((bx, by));
            self.sensormap.insert((sx, sy));
            let min_x = min(sx - dist, bx);
            let min_y = min(sy - dist, by);
            let max_x = max(sx + dist, bx);
            let max_y = max(sy + dist, by);
            self.min_x = min(self.min_x, min_x);
            self.min_y = min(self.min_x, min_y);
            self.max_x = max(self.max_x, max_x);
            self.max_y = max(self.max_y, max_y);
        }
    }
    fn is_coordinate_beacon_free(&self, coord: (i32, i32)) -> bool {
        if self.beacons.contains(&coord) {
            return false;
        }
        for sensor in self.sensors.iter() {
            if calc_dist(coord, sensor.coord) <= sensor.closest_beacon_dist {
                return true;
            }
        }
        return false;
    }

    fn count_beacon_free_row(&self, row: i32) -> u32 {
        let mut result = 0;
        for x in self.min_x..=self.max_x {
            if self.is_coordinate_beacon_free((x, row)) {
                result += 1;
            }
        }
        result
    }

    fn draw_cave(&self) {
        println!(
            "({},{}), ({}, {})",
            self.min_x - 1,
            self.min_y - 1,
            self.max_x + 1,
            self.max_y + 1
        );
        for y in (self.min_y - 1)..=(self.max_y + 1) {
            for x in (self.min_x - 1)..=(self.max_x + 1) {
                if self.beacons.contains(&(x, y)) {
                    print!("B");
                } else if self.sensormap.contains(&(x, y)) {
                    print!("S");
                } else if self.is_coordinate_beacon_free((x, y)) {
                    print!("#");
                } else {
                    print!(".");
                }
            }
            print!("\n");
        }
    }
}

fn solve_puzzle(input_string: &String, row: i32) -> u32 {
    let mut cave: Cave = Default::default();

    cave.init_from_string(input_string);
    //cave.draw_cave();
    cave.count_beacon_free_row(row)
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 26;

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
    let result = solve_puzzle(&test_input_string, 10);
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
    let result = solve_puzzle(&real_input_string, 2000000);
    println!("Real Result : {}", result);
}
