use std::{
    cmp::{max, min},
    collections::{HashMap, HashSet},
};

#[derive(Debug, Default)]
struct Valve {
    flow_rate: u32,
    tunnels: Vec<u32>,
}

#[derive(Debug, Default, Copy, Clone)]
struct Worker {
    time_left: i32,
    valve: u32,
    flow: u32,
}

struct State {
    open_valves: HashSet<u32>,
    best_score: u32,
    state_visisted_count: u32,
}

impl Default for State {
    fn default() -> Self {
        State {
            open_valves: HashSet::new(),
            state_visisted_count: 0,
            best_score: 0,
        }
    }
}

struct Cave {
    name_map: HashMap<String, u32>,
    valves: Vec<(u32, Valve)>,
    distances: HashMap<(u32, u32), u32>,
    interesting_valves: Vec<(u32, u32)>,
    valve_count: u32,
    max_flow: u32,
}

impl Default for Cave {
    fn default() -> Self {
        Cave {
            interesting_valves: Vec::new(),
            distances: HashMap::new(),
            name_map: HashMap::new(),
            valve_count: 0,
            max_flow: 0,
            valves: Vec::new(),
        }
    }
}

impl Cave {
    fn find_distances(&mut self) {
        for (id, v) in self.valves.iter() {
            self.distances.insert((*id, *id), 0);
            for v2 in v.tunnels.iter() {
                self.distances.insert((*id, *v2), 1);
            }
        }

        for k in 1..=self.valve_count {
            for i in 1..=self.valve_count {
                for j in 1..=self.valve_count {
                    let dist_ik = match self.distances.get(&(i, k)) {
                        Some(d) => *d,
                        None => continue,
                    };
                    let dist_kj = match self.distances.get(&(k, j)) {
                        Some(d) => *d,
                        None => continue,
                    };
                    let dist_ij = match self.distances.get(&(i, j)) {
                        Some(d) => min(*d, dist_ik + dist_kj),
                        None => dist_ik + dist_kj,
                    };

                    self.distances.insert((i, j), dist_ij);
                }
            }
        }
    }

    fn init_from_string(&mut self, input_string: &String) {
        for line in input_string.lines() {
            let mut valve: Valve = Default::default();
            let sp = match line.split_once("; tunnels lead to valves ") {
                Some(x) => x,
                None => line.split_once("; tunnel leads to valve ").unwrap(),
            };

            let (name, flow_rate) =
                sscanf::sscanf!(sp.0, "Valve {} has flow rate={}", str, u32).unwrap();
            let valve_id = match self.name_map.get(&name.to_string()) {
                Some(id) => *id,
                None => {
                    self.valve_count += 1;
                    self.name_map.insert(name.to_string(), self.valve_count);
                    self.valve_count
                }
            };
            valve.flow_rate = flow_rate;

            let nexts = sp.1.split(", ");
            for next in nexts {
                let id = match self.name_map.get(&next.to_string()) {
                    Some(i) => *i,
                    None => {
                        self.valve_count += 1;
                        self.name_map.insert(next.to_string(), self.valve_count);
                        self.valve_count
                    }
                };
                valve.tunnels.push(id);
            }

            if valve.flow_rate > 0 {
                self.max_flow += valve.flow_rate;
                self.interesting_valves.push((valve_id, valve.flow_rate));
            }
            self.valves.push((valve_id, valve));
        }
        self.interesting_valves.sort_by(|a, b| a.1.cmp(&b.1));
        self.interesting_valves.reverse();
    }

    fn make_next_move(
        &self,
        state: &mut State,
        workers: &Vec<Worker>,
        score_so_far: u32,
        flow_left: u32,
    ) {
        state.state_visisted_count += 1;
        let mut new_workers = workers.clone();
        new_workers.sort_by(|a, b| a.time_left.cmp(&b.time_left));
        new_workers.reverse();
        let worker = new_workers[0];
        let time_left = worker.time_left;
        let current_valve = worker.valve;
        let current_flow = worker.flow;

        if time_left <= 0 {
            state.best_score = max(state.best_score, score_so_far);
            return;
        }
        let mut new_time_left = time_left;
        let mut new_score = score_so_far;

        if current_flow > 0 {
            //
            // Turn on the valve and calc score
            //
            new_time_left -= 1;
            let score_for_this_valve = current_flow * (new_time_left as u32);
            new_score += score_for_this_valve;
        }

        let new_flow_left = flow_left - current_flow;
        state.best_score = max(state.best_score, new_score);
        state.best_score = max(state.best_score, new_score);
        new_workers[0].flow = current_flow;
        new_workers[0].valve = current_valve;
        new_workers[0].time_left = 0;
        self.make_next_move(state, &new_workers, new_score, new_flow_left);
        //if state.open_valves.len() == self.interesting_valves.len() {

        //    return;
        //}

        let theor_max = new_flow_left * (new_time_left as u32);

        if new_score + theor_max < state.best_score {
            return;
        }

        for i in 0..self.interesting_valves.len() {
            let (id, flow) = self.interesting_valves.get(i).unwrap().clone();
            if state.open_valves.contains(&id) {
                continue;
            }
            assert!(id != current_valve);
            let time = *self.distances.get(&(current_valve, id)).unwrap();
            if time > (new_time_left as u32) {
                continue;
            }
            //assert!(time > 0);
            state.open_valves.insert(id);
            new_workers[0].flow = flow;
            new_workers[0].valve = id;
            new_workers[0].time_left = new_time_left - (time as i32);
            state.open_valves.insert(id);
            self.make_next_move(state, &new_workers, new_score, new_flow_left);
            state.open_valves.remove(&id);
        }
    }

    fn find_solution(&mut self, starting_valve: &String, time_limit: u32) -> u32 {
        let start_id = self.name_map.get(starting_valve).unwrap();
        let workers = vec![
            Worker {
                time_left: time_limit as i32,
                valve: *start_id,
                flow: 0,
            },
            Worker {
                time_left: time_limit as i32,
                valve: *start_id,
                flow: 0,
            },
        ];
        let mut state: State = Default::default();

        self.make_next_move(&mut state, &workers, 0, self.max_flow);
        println!("{}", state.state_visisted_count);

        state.best_score
    }
}

fn solve_puzzle(input_string: &String) -> u32 {
    let mut cave: Cave = Default::default();
    cave.init_from_string(input_string);
    cave.find_distances();
    let start = "AA";

    let result = cave.find_solution(&start.to_string(), 26);

    result
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 1707;

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
