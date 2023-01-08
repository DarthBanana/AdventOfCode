use std::{
    cmp::{max, min},
    ops::{Add, Mul, Sub},
};

#[derive(Default, Clone, Copy)]
struct Properties {
    capacity: i64,
    durability: i64,
    flavor: i64,
    texture: i64,
}
impl Add for Properties {
    type Output = Properties;

    fn add(self, other: Properties) -> Properties {
        Properties {
            capacity: self.capacity + other.capacity,
            durability: self.durability + other.durability,
            flavor: self.flavor + other.flavor,
            texture: self.texture + other.texture,
        }
    }
}

impl Sub for Properties {
    type Output = Properties;

    fn sub(self, other: Properties) -> Properties {
        Properties {
            capacity: self.capacity - other.capacity,
            durability: self.durability - other.durability,
            flavor: self.flavor - other.flavor,
            texture: self.texture - other.texture,
        }
    }
}
impl Mul<i64> for Properties {
    type Output = Properties;

    fn mul(self, other: i64) -> Properties {
        Properties {
            capacity: self.capacity * other,
            durability: self.durability * other,
            flavor: self.flavor * other,
            texture: self.texture * other,
        }
    }
}

impl Properties {
    fn calc_score(&self) -> i64 {
        max(self.capacity, 0) * max(self.durability, 0) * max(self.flavor, 0) * max(self.texture, 0)
    }
}

struct Ingredient {
    name: String,
    properties: Properties,
    calories: i64,
}

#[derive(Default)]
struct Puzzle {
    ingredients: Vec<Ingredient>,
    proportions: Vec<i64>,
    max_score: i64,
}

impl Puzzle {
    fn init_from_string(&mut self, input_string: &String) {
        for line in input_string.lines() {
            let (name, capacity, durability, flavor, texture, calories) = sscanf::sscanf!(
                line,
                "{}: capacity {}, durability {}, flavor {}, texture {}, calories {}",
                String,
                i64,
                i64,
                i64,
                i64,
                i64
            )
            .unwrap();

            let new_ingredient = Ingredient {
                name,
                properties: Properties {
                    capacity,
                    durability,
                    flavor,
                    texture,
                },
                calories,
            };
            self.ingredients.push(new_ingredient);
        }
    }
    fn calc_score(&self) -> i64 {
        //println!("New Recipe:");
        let mut recipe_props: Properties = Default::default();
        for i in 0..self.proportions.len() {
            let this_ingredient_props = self.ingredients[i].properties * self.proportions[i];
            recipe_props = recipe_props + this_ingredient_props;
            //println!("  {}: {}", self.ingredients[i].name, self.proportions[i]);
        }
        let score = recipe_props.calc_score();
        //println!("  Score: {}", score);
        score
    }

    fn add_next_ingredient(&mut self, index: usize, size_left: i64) {
        if size_left == 0 {
            self.max_score = max(self.max_score, self.calc_score());
            return;
        }

        if index == self.ingredients.len() - 1 {
            self.proportions.push(size_left);
            self.max_score = max(self.max_score, self.calc_score());
            self.proportions.pop();
            return;
        }
        for i in 0..size_left {
            self.proportions.push(i);
            self.add_next_ingredient(index + 1, size_left - i);
            self.proportions.pop();
        }
    }

    fn find_recipe(&mut self) {
        self.add_next_ingredient(0, 100);
    }
}
fn solve_puzzle(input_string: &String) -> i64 {
    let mut puzzle: Puzzle = Default::default();

    puzzle.init_from_string(input_string);
    puzzle.find_recipe();
    puzzle.max_score
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 62842880;

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
