use std::{
    cmp::max,
    collections::{HashMap, HashSet},
};

#[derive(Debug, Copy, Clone)]
enum Direction {
    Left,
    Right,
    Down,
}

#[derive(Debug, Default, Clone)]
struct Shape {
    points: Vec<(u32, u32)>,
    height: u32,
    width: u32,
}

#[derive(Debug, Default, Clone)]
struct Rock {
    shape: Shape,
    position: (u32, u64),
}

#[derive(Debug, Clone)]
struct State {
    solids: HashSet<(u32, u64)>,
    highest_solid: u64,
    shape_index: usize,
    jet_index: usize,
    history: HashMap<(Vec<u16>, usize, usize), (u64, u64)>,
    rock_count: u64,
}

impl Default for State {
    fn default() -> Self {
        State {
            solids: HashSet::new(),
            history: HashMap::new(),
            highest_solid: 0,
            shape_index: 0,
            jet_index: 0,
            rock_count: 0,
        }
    }
}

#[derive(Debug, Clone)]
struct Cave {
    shapes: Vec<Shape>,
    jets: Vec<Direction>,
    cave_width: u32,
    top_count: u32,
}

impl Default for Cave {
    fn default() -> Self {
        Cave {
            shapes: Vec::new(),
            jets: Vec::new(),
            cave_width: 7,
            top_count: 30,
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
            position: (2, state.highest_solid + 3),
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
                if rock.position.0 + rock.shape.width == self.cave_width - 1 {
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
            if state
                .solids
                .contains(&(new_pos.0 + i.0, new_pos.1 + i.1 as u64))
            {
                return false;
            }
        }
        rock.position = new_pos;
        return true;
    }

    fn stop_rock(&self, state: &mut State, rock: &Rock) {
        for p in rock.shape.points.iter() {
            let new_p = (rock.position.0 + p.0, rock.position.1 + p.1 as u64);
            state.solids.insert(new_p);
        }
        state.highest_solid = max(
            state.highest_solid,
            (rock.position.1 as u64 + (rock.shape.height as u64) + 1) as u64,
        );
    }

    fn cycle_check(&self, state: &mut State) -> Option<(u64, u64)> {
        let mut history_sig: Vec<u16> = Vec::new();
        if state.rock_count < 100 {
            return None;
        }
        for y in (state.highest_solid - (self.top_count as u64))..=state.highest_solid {
            let mut v: u16 = 0;
            for x in 0..=self.cave_width {
                if state.solids.contains(&(x, y)) {
                    v |= 1 << x;
                }
            }
            history_sig.push(v);
        }
        let result = state.history.insert(
            (history_sig, state.shape_index, state.jet_index),
            (state.rock_count, state.highest_solid),
        );

        result
    }

    fn drop_next_rock(&self, state: &mut State) {
        let mut new_rock = self.get_next_rock(state);

        loop {
            let new_jet = self.get_next_jet(state);
            self.try_to_push_rock(state, &mut new_rock, new_jet);
            if self.try_to_push_rock(state, &mut new_rock, Direction::Down) == false {
                break;
            }
        }

        self.stop_rock(state, &new_rock);

        state.rock_count += 1;
    }

    fn drop_rocks(&self, state: &mut State, count: u64) -> u64 {
        let mut cycle_found = false;

        while state.rock_count < count {
            self.drop_next_rock(state);

            if !cycle_found && state.shape_index == 0 {
                if let Some((prev_rock, prev_height)) = self.cycle_check(state) {
                    cycle_found = true;
                    println!("CYCLE_FOUND {}", state.rock_count);
                    self.draw_some(state, prev_height);
                    let cycle_size = state.rock_count - prev_rock;
                    let cycles = (count - state.rock_count) / cycle_size;
                    state.rock_count += cycles * cycle_size;
                    println!("jumping to rock {}", state.rock_count);
                    self.draw_some(state, state.highest_solid);
                    let copy_from =
                        (state.highest_solid - self.top_count as u64)..=state.highest_solid;
                    let copy_offset = (state.highest_solid - prev_height) * cycles;
                    for y in copy_from {
                        for x in 0..self.cave_width {
                            match state.solids.get(&(x, y)) {
                                Some(s) => {
                                    state.solids.insert((s.0, s.1 + copy_offset));
                                }
                                None => (),
                            }
                        }
                    }
                    state.highest_solid += copy_offset;
                    self.draw_some(state, state.highest_solid);
                }
            }
        }
        state.highest_solid
    }

    fn draw_some(&self, state: &State, top_row: u64) {
        println!("{}", top_row);
        for y in (top_row - self.top_count as u64)..=top_row {
            print!("|");
            for x in 0..self.cave_width {
                if state.solids.contains(&(x, top_row - y)) {
                    print!("#");
                } else {
                    print!(".");
                }
            }
            print!("|\n");
        }
    }
    fn draw(&self, state: &State) {
        for y in 0..=state.highest_solid {
            print!("|");
            for x in 0..self.cave_width {
                if state.solids.contains(&(x, state.highest_solid - y)) {
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

fn solve_puzzle(input_string: &String) -> u64 {
    let mut cave: Cave = Default::default();
    let mut state: State = Default::default();
    cave.build_shapes();
    cave.init_from_string(input_string);

    let result = cave.drop_rocks(&mut state, 1000000000000);
    result
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 1514285714288;

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
