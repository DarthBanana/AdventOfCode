use std::{cmp::max, collections::HashSet};

#[derive(Debug, Copy, Clone)]
enum Direction {
    Left,
    Right,
    Down,
}

#[derive(Debug, Default, Clone)]
struct Shape {
    points: Vec<(i32, i32)>,
    height: u32,
    width: u32,
}

#[derive(Debug, Default, Clone)]
struct Rock {
    shape: Shape,
    position: (i32, i32),
}

#[derive(Debug, Clone)]
struct State {
    solids: HashSet<(i32, i32)>,
    highest_solid: u32,
    shape_index: usize,
    jet_index: usize,
}

impl Default for State {
    fn default() -> Self {
        State {
            solids: HashSet::new(),
            highest_solid: 0,
            shape_index: 0,
            jet_index: 0,
        }
    }
}

#[derive(Debug, Clone)]
struct Cave {
    shapes: Vec<Shape>,
    jets: Vec<Direction>,
    cave_width: u32,
}

impl Default for Cave {
    fn default() -> Self {
        Cave {
            shapes: Vec::new(),
            jets: Vec::new(),
            cave_width: 7,
        }
    }
}

impl Cave {
    fn build_shapes(&mut self) {
        let flat = Shape {
            points: vec![(0, 0), (1, 0), (2, 0), (3, 0)],
            height: 0,
            width: 3,
        };
        let plus = Shape {
            points: vec![(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
            height: 2,
            width: 2,
        };
        let el = Shape {
            points: vec![(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
            height: 2,
            width: 2,
        };
        let tall = Shape {
            points: vec![(0, 0), (0, 1), (0, 2), (0, 3)],
            height: 3,
            width: 0,
        };
        let square = Shape {
            points: vec![(0, 0), (1, 0), (0, 1), (1, 1)],
            height: 1,
            width: 1,
        };
        self.shapes.push(flat);
        self.shapes.push(plus);
        self.shapes.push(el);
        self.shapes.push(tall);
        self.shapes.push(square);
    }

    fn init_from_string(&mut self, input_string: &String) {
        for c in input_string.chars() {
            match c {
                '>' => self.jets.push(Direction::Right),
                '<' => self.jets.push(Direction::Left),
                _ => panic!("Bad input character"),
            };
        }
    }

    fn get_next_rock(&self, state: &mut State) -> Rock {
        let new_rock = Rock {
            shape: self.shapes[state.shape_index].clone(),
            position: (2, (state.highest_solid + 3) as i32),
        };
        state.shape_index += 1;
        state.shape_index %= self.shapes.len();
        new_rock
    }

    fn get_next_jet(&self, state: &mut State) -> Direction {
        let jet = self.jets[state.jet_index];
        state.jet_index += 1;
        state.jet_index %= self.jets.len();
        jet
    }

    fn try_to_push_rock(&self, state: &State, rock: &mut Rock, direction: Direction) -> bool {
        let new_pos = match direction {
            Direction::Left => {
                if rock.position.0 == 0 {
                    return false;
                }
                (rock.position.0 - 1, rock.position.1)
            }

            Direction::Right => {
                if rock.position.0 + (rock.shape.width as i32) == (self.cave_width as i32) - 1 {
                    return false;
                }
                (rock.position.0 + 1, rock.position.1)
            }
            Direction::Down => {
                if rock.position.1 == 0 {
                    return false;
                }
                (rock.position.0, rock.position.1 - 1)
            }
        };
        for i in rock.shape.points.iter() {
            if state.solids.contains(&(new_pos.0 + i.0, new_pos.1 + i.1)) {
                return false;
            }
        }
        rock.position = new_pos;
        return true;
    }

    fn stop_rock(&self, state: &mut State, rock: &Rock) {
        for p in rock.shape.points.iter() {
            let new_p = (rock.position.0 + p.0, rock.position.1 + p.1);
            state.solids.insert(new_p);
        }
        state.highest_solid = max(
            state.highest_solid,
            (rock.position.1 as u32 + rock.shape.height + 1) as u32,
        );
    }

    fn drop_rocks(&self, state: &mut State, count: u32) {
        for _i in 0..count {
            let mut new_rock = self.get_next_rock(state);

            loop {
                let new_jet = self.get_next_jet(state);
                self.try_to_push_rock(state, &mut new_rock, new_jet);
                if self.try_to_push_rock(state, &mut new_rock, Direction::Down) == false {
                    break;
                }
            }
            self.stop_rock(state, &new_rock);
        }
    }

    fn draw(&self, state: &State) {
        for y in 0..=state.highest_solid {
            print!("|");
            for x in 0..self.cave_width {
                if state
                    .solids
                    .contains(&(x as i32, (state.highest_solid - y) as i32))
                {
                    print!("#");
                } else {
                    print!(".");
                }
            }
            print!("|\n");
        }
        println!("+-------+");
    }
}

fn solve_puzzle(input_string: &String) -> u32 {
    let mut cave: Cave = Default::default();
    let mut state: State = Default::default();
    cave.build_shapes();
    cave.init_from_string(input_string);

    cave.drop_rocks(&mut state, 2022);

    state.highest_solid
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 3068;

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
