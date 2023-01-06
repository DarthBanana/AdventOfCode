use std::{
    cmp::max,
    collections::{HashMap, VecDeque},
};

#[derive(Clone, Debug, Default)]
struct Guest {
    name: String,
    id: usize,
    guest_scores: HashMap<usize, i64>,
    max_score: i64,
}

#[derive(Clone, Debug, Default)]
struct State {
    highest_score: i64,
    available_list: VecDeque<usize>,
    seated_list: Vec<usize>,
    score_so_far: i64,
}

#[derive(Clone, Debug)]
struct Puzzle {
    name_map: HashMap<String, usize>,
    guests: HashMap<usize, Guest>,
    next_id: usize,
}
impl Default for Puzzle {
    fn default() -> Self {
        Puzzle {
            name_map: HashMap::new(),
            guests: HashMap::new(),
            next_id: 0,
        }
    }
}

impl Puzzle {
    fn get_id_from_name(&mut self, name: &String) -> usize {
        match self.name_map.get(name) {
            Some(i) => *i,
            None => {
                let new_id = self.next_id;
                self.next_id += 1;
                self.name_map.insert(name.clone(), new_id);
                new_id
            }
        }
    }

    fn init_from_string(&mut self, input_string: &String) {
        let mut guests: HashMap<usize, Guest> = HashMap::new();
        for line in input_string.lines() {
            let (guest_name, direction, value, neighbor_name) = sscanf::sscanf!(
                line,
                "{} would {} {} happiness units by sitting next to {}.",
                String,
                String,
                i64,
                String
            )
            .unwrap();
            let guest_id = self.get_id_from_name(&guest_name);

            let mut guest = match guests.remove(&guest_id) {
                Some(g) => g,
                None => {
                    let mut g = Guest {
                        name: guest_name.clone(),
                        id: guest_id,
                        guest_scores: HashMap::new(),
                        max_score: i64::MIN,
                    };
                    g
                }
            };
            let mut score = value;
            if direction.contains("lose") {
                score *= -1;
            }
            guest.max_score = max(guest.max_score, score);
            let neighbor = self.get_id_from_name(&neighbor_name);
            guest.guest_scores.insert(neighbor, score);
            guests.insert(guest_id, guest);
        }

        for g in guests.drain() {
            self.guests.insert(g.0, g.1);
        }
    }

    fn seat_the_rest(&self, state: &mut State) {
        if state.available_list.is_empty() {
            //
            // Calculate the score
            //
            let mut total_score = 0;
            for i in 0..state.seated_list.len() {
                let cur_guest_id = state.seated_list[i];
                let cur_guest = self.guests.get(&cur_guest_id).unwrap();

                if i > 0 {
                    let prev = ((i + state.seated_list.len()) - 1) % state.seated_list.len();
                    let prev_guest_id = state.seated_list[prev];
                    total_score += cur_guest.guest_scores.get(&prev_guest_id).unwrap();
                }
                if i < (state.seated_list.len() - 1) {
                    let next = (i + 1) % state.seated_list.len();

                    let next_guest_id = state.seated_list[next];

                    total_score += cur_guest.guest_scores.get(&next_guest_id).unwrap();
                }
            }
            state.highest_score = max(state.highest_score, total_score);
        }

        if !state.seated_list.is_empty() {
            //
            // Check the max remaining score:
            //
            let mut theor_max = state.score_so_far;
            theor_max += self
                .guests
                .get(state.seated_list.last().unwrap())
                .unwrap()
                .max_score;
            for g in state.available_list.iter() {
                theor_max += 2 * self.guests.get(&g).unwrap().max_score;
            }
            if theor_max < state.highest_score {
                return;
            }
        }

        //
        // try each next guest
        //
        for i in 0..state.available_list.len() {
            let g = state.available_list.pop_front().unwrap();
            let mut score_delta = 0;

            if !state.seated_list.is_empty() {
                score_delta = *self
                    .guests
                    .get(&g)
                    .unwrap()
                    .guest_scores
                    .get(state.seated_list.last().unwrap())
                    .unwrap();

                score_delta += *self
                    .guests
                    .get(state.seated_list.last().unwrap())
                    .unwrap()
                    .guest_scores
                    .get(&g)
                    .unwrap();
            }

            state.seated_list.push(g);
            state.score_so_far += score_delta;

            self.seat_the_rest(state);
            state.score_so_far -= score_delta;
            let g = state.seated_list.pop().unwrap();

            state.available_list.push_back(g);
        }
    }
}

fn solve_puzzle(input_string: &String) -> i64 {
    let mut result = 0;
    let mut puzzle: Puzzle = Default::default();
    let mut state: State = Default::default();

    puzzle.init_from_string(input_string);

    for i in 0..puzzle.next_id {
        state.available_list.push_back(i);
    }
    puzzle.seat_the_rest(&mut state);

    result = state.highest_score;
    result
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 286;

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
